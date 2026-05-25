from config.logging import logger

# creating a fallback quiz
def create_fallback_quiz(subject,number_of_questions):
    '''Helper function to create a fallback quiz if parsing fails'''

    logger.warning(f"Using fallback quiz generation for {subject} with {number_of_questions} questions.")

    return [
        {
            "question": f"Sample {subject} question #{i+1}",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct_answer": "Option A",
            "explanation": "This is a fallback explanation."
        }
        for i in range(number_of_questions)
    ]