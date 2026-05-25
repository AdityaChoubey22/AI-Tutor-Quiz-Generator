import time
import random
import re
from langchain_core.messages import HumanMessage
from openai import RateLimitError
from llm_invoke.llm import get_llm
from validation.parsing_response import parse_quiz_response
from validation.create_fallback import create_fallback_quiz
from config.logging import logger
from utils.quiz_formatter import format_quiz_for_reveal
from utils.prompt_utils import create_quiz_prompt

# generating the quiz
def generate_quiz(subject, level, number_of_questions=5, reveal_answer=True):
    """
    Generate a quiz with multiple-choice questions based on subject and level.

    Args:
        subject (str): The academic subject
        level (str): Learning level (Beginner, Intermediate, Advanced)
        number_of_questions (int): Number of questions to generate
        reveal_answer (bool): Whether to format the response with
        hidden answers that can be revealed

    Returns:
        dict: Contains quiz data (list of questions) and formatted HTML if reveal_answer is True
    """
    try:
        llm = get_llm()
        all_quiz_data = []
        
        # Check if we are using the keyless Pollinations fallback
        is_pollinations = llm.__class__.__name__ == "PollinationsLLM"
        
        # Pollinations requires very small chunks to prevent JSON truncation.
        # Gemini can handle up to 25.
        chunk_size = 3 if is_pollinations else 25
        
        # Calculate how many successful chunks we need
        needed_chunks = (number_of_questions + chunk_size - 1) // chunk_size
        
        attempts = 0
        # Give ourselves extra attempts in case some API calls fail or return duplicates
        max_attempts = needed_chunks * 3
        
        logger.info(f"Starting quiz generation for subject: {subject}, level: {level}, total questions: {number_of_questions}")
        
        while len(all_quiz_data) < number_of_questions and attempts < max_attempts:
            attempts += 1
            
            # Determine current chunk size
            current_batch_size = min(chunk_size, number_of_questions - len(all_quiz_data))
            
            # If we need very few questions, generate exactly that
            if current_batch_size <= 0:
                break
                
            # Create a string of existing question titles to help LLM avoid them
            existing_questions_str = ""
            if all_quiz_data:
                existing_titles = [q["question"] for q in all_quiz_data]
                existing_questions_str = "Avoid generating any of the following questions (they already exist in the quiz):\n" + "\n".join(f"- {title}" for title in existing_titles[-40:])
            
            prompt = create_quiz_prompt(subject, level, current_batch_size)
            if existing_questions_str:
                prompt += f"\n\nCRITICAL: {existing_questions_str}\nMake sure all generated questions are unique and distinct from the above."
            
            # To ensure even more diversity, we can add a slight randomization instruction to the prompt
            prompt += f"\n\nRandomization key: {random.randint(1, 1000000)}. Generate a diverse and unique set of questions."
            
            logger.info(f"Generating batch {attempts}/{max_attempts}: requesting {current_batch_size} questions (topic: {subject}, level: {level})")
            
            # If using keyless Pollinations, we must sleep to prevent IP bans
            if is_pollinations and attempts > 1:
                logger.info("Sleeping for 3s to prevent keyless rate limits...")
                time.sleep(3.0)
                
            try:
                response = llm.invoke([HumanMessage(content=prompt)])
                
                # Parse current batch without fallback (fallback=False) so we can validate it
                batch_data = parse_quiz_response(response.content, subject, current_batch_size, fallback=False)
                
                if batch_data and isinstance(batch_data, list):
                    valid_batch = []
                    for q in batch_data:
                        try:
                            # Validate question structure
                            if (isinstance(q, dict) and 
                                    all(k in q for k in ["question", "options", "correct_answer"]) and 
                                    isinstance(q["options"], list) and len(q["options"]) == 4):
                                
                                # Normalize correct_answer if it's a letter/option indicator like "A", "B", "C", "D" or "Option A"
                                correct = str(q.get("correct_answer", "")).strip()
                                options = q["options"]
                                
                                if correct in options:
                                    pass
                                else:
                                    # Try to extract the option letter/index
                                    match = re.search(r'\b(Option\s+)?([A-D])\b', correct, re.IGNORECASE)
                                    if match:
                                        letter = match.group(2).upper()
                                        idx = ord(letter) - ord('A')
                                        if 0 <= idx < len(options):
                                            q["correct_answer"] = options[idx]
                                    else:
                                        # Check if index number string (like "0", "1", "2", "3")
                                        try:
                                            idx = int(correct)
                                            if 0 <= idx < len(options):
                                                q["correct_answer"] = options[idx]
                                        except ValueError:
                                            pass
                                
                                # Check for duplicates
                                is_duplicate = any(
                                    q["question"].strip().lower() == eq["question"].strip().lower() 
                                    for eq in all_quiz_data
                                )
                                if not is_duplicate:
                                    if "explanation" not in q or not q["explanation"]:
                                        q["explanation"] = f"The correct answer is {q['correct_answer']}."
                                    valid_batch.append(q)
                                else:
                                    logger.info(f"Skipping duplicate question: {q['question']}")
                        except Exception as ve:
                            logger.warning(f"Validation error for question: {ve}")
                            continue
                            
                    all_quiz_data.extend(valid_batch)
                    logger.info(f"Batch {attempts} successful: gathered {len(valid_batch)} new unique questions. Total so far: {len(all_quiz_data)}/{number_of_questions}")
                else:
                    logger.warning(f"Batch {attempts} returned empty or invalid data.")
            except RateLimitError:
                logger.error("OpenAI rate limit exceeded.")
                raise Exception("Rate limit exceeded. Please check your OpenAI usage or try again later.")
            except Exception as e:
                logger.error(f"Error in batch {attempts}: {str(e)}")
                sleep_dur = 3.0 if is_pollinations else 2.0
                logger.info(f"Sleeping for {sleep_dur}s before retry...")
                time.sleep(sleep_dur)
                continue
                
        # If we failed to generate any questions, use fallback
        if not all_quiz_data:
            logger.warning("Failed to generate any questions, using fallback.")
            all_quiz_data = create_fallback_quiz(subject, number_of_questions)
        elif len(all_quiz_data) < number_of_questions:
            # Pad with backup questions if LLM failed to reach target count
            logger.warning(f"Only generated {len(all_quiz_data)}/{number_of_questions} questions. Padding with fallback.")
            padding_needed = number_of_questions - len(all_quiz_data)
            fallback_padding = create_fallback_quiz(subject, padding_needed)
            for i, q in enumerate(fallback_padding):
                q["question"] = f"Backup {subject} question #{len(all_quiz_data) + i + 1}"
            all_quiz_data.extend(fallback_padding)
            
        # Ensure we return exactly the requested number of questions
        all_quiz_data = all_quiz_data[:number_of_questions]
        
        # Format the quiz data for HTML display if required
        if reveal_answer:
            formatted_quiz = format_quiz_for_reveal(all_quiz_data)
            return {
                "quiz_data": all_quiz_data, 
                "formatted_quiz": formatted_quiz
            }
        else:
            return {
                "quiz_data": all_quiz_data
            }
    except Exception as e:
        logger.error(f"Error generating quiz: {str(e)}")
        raise Exception(f"Failed to generate quiz: {str(e)}")
