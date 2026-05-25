# parsing the quiz response
import json
import re
from validation.create_fallback import create_fallback_quiz
from validation.quiz_data_validation import validate_quiz_data
from config.logging import logger


def parse_quiz_response(response_content, subject, number_of_questions, fallback=True):
    '''Helper function to parse the quiz and validate the quiz response'''
    try:
        # try to find json content using regex
        json_match = re.search(r'```json\s*(\[[\s\S]*?\])\s*```',response_content)

        if json_match:
            # extract json from code block
            quiz_json = json_match.group(1)
        else:
            # try to find raw json array
            json_match = re.search(r'\[\s*\{.*\}\s*\]',response_content,re.DOTALL)
            if json_match:
                quiz_json = json_match.group(0)
            else:
                # assume the entire response is json
                quiz_json = response_content
        # Parse the json content
        quiz_data = json.loads(quiz_json)

        # Validate the quiz data
        validate_quiz_data(quiz_data)

        # Ensure we have the request number of questions
        if len(quiz_data) > number_of_questions:
            quiz_data = quiz_data[:number_of_questions]
        # Add explaination field if missing
        for question in quiz_data:
            if "explanation" not in question:
                question["explanation"] = f"The correct answer is {question['correct_answer']}."
        return quiz_data
    except(json.JSONDecodeError, ValueError) as e:
        logger.error(f"Error parsing quiz response: {str(e)}")
        if fallback:
            # Fallback to a simple quiz if parsing fails
            return create_fallback_quiz(subject, number_of_questions)
        else:
            raise e
