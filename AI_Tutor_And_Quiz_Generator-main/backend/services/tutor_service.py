from langchain_core.messages import HumanMessage
from openai import RateLimitError
from config.logging import logger
from llm_invoke.llm import get_llm
from utils.tutor_formatter import format_tutoring_response
from utils.prompt_utils import create_tutoring_prompt

# Generating the reponse of the Tutor
def generate_tutoring_response(subject, level, question, learning_style, background_knowledge, language):
    """
    Generate a personalized tutoring response based on the user prefrences.
    
    Args:
        subject (str): The subject of the question.
        level (str): The level of the question(Beginner, Intermediate, Advanced).
        question (str): The question to be answered.
        learning_style (str): The user's preferred learning style.
        background_knowledge (str): The user's background knowledge.
        language (str): The language in which the response should be generated.

    Returns:
        str: The generated response from the AI model.
    """
    try:
        # getting the LLM instance
        llm = get_llm()

        # Construct an effective prompt
        prompt = create_tutoring_prompt(subject, level, question, learning_style, background_knowledge, language)

        # generate response with error handling
        logger.info(f"Generating response for subject: {subject}, level: {level}")
        try:
            response = llm.invoke([HumanMessage(content=prompt)])
        except RateLimitError as e:
            logger.error("OpenAI rate limit exceeded.")
            raise Exception("Rate limit exceeded. Please check your OpenAI usage or try again later.")

        # Post-process the response based on the learning style
        return format_tutoring_response(response.content, learning_style)
    
    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        raise Exception(f"Failed to generate response: {str(e)}")

