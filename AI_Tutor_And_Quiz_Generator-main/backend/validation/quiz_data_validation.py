# validate quiz data
def validate_quiz_data(quiz_data):
    '''Helper function to validate the quiz data structure'''
    if not isinstance(quiz_data, list):
        raise ValueError("Quiz data must be a list of questions.")
    
    for question in quiz_data:
        if not isinstance(question, dict):
            raise ValueError("Each question must be a dictionary.")
        
        if not all(key in question for key in ["question","options","correct_answer"]):
            raise ValueError("Each question must contain question, options, and correct_answer keys.")
        
        if not isinstance(question["options"], list) or len(question["options"]) != 4:
            raise ValueError("Each question must have exactly 4 options.")