# generating the prompt for the quiz
def create_quiz_prompt(subject, level, number_of_questions):
    '''Helper function to create a well-structured quiz generation prompt'''

    difficulty_instructions = ""
    if level == "Advanced":
        difficulty_instructions = """
    - CRITICAL: The difficulty MUST be extremely high, equivalent to competitive exams like GATE (Graduate Aptitude Test in Engineering), IIT-JEE, or difficult university final exams.
    - Include complex numerical problems, multi-step logical reasoning, and theoretical edge-cases.
    - DO NOT generate simple definition-based or trivial questions.
    - The options must be highly plausible to confuse a well-prepared student (strong distractors).
        """

    return f"""
    Create a {level}-level quiz on {subject} with exactly {number_of_questions} multiple-choice questions.

    INSTRUCTIONS:
    1. Each question should be appropriate for the {level} level students. {difficulty_instructions}
    2. Each question must have exactly 4 answer options(A, B, C, D)
    3. Clearly indicate the correct answer
    4. Cover distinct aspects of the {subject}

    FORMAT YOUR RESPONSE AS JSON:
    ```json
    [
        {
            {
                "question": "Question text",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct_answer": "Option A",
                "explanation": "Brief explanation of why this answer is correct"
            }
        },
        ...
    ]
    ```
    IMPORTANT: Make sure to return valid JSON that can be parsed.
    Do not include any text outside the JSON array.
    Include a brief explanation for each correct answer.
    """

# generating the prompt for the tutor
def create_tutoring_prompt(subject, level, question, learning_style, background_knowledge, language):
    """Helper function to create a well-structured prompt for the AI model."""
    # Build prompt using all necessary context and instructions
    prompt = f"""
    You are an expert tutor in {subject} at the {level} level.

    STUDENTS PROFILE:
    - Background Knowledge: {background_knowledge}
    - Learning Style prefrence: {learning_style}
    - Language Preference: {language}

    QUESTION:
    {question}

    INSTRUCTIONS:
    1. Provide a clear, educational explanation that directly addresses the question
    2. Tailor your response to a {background_knowledge} student at the {level} level
    3. Use {language} as the primary language
    4. Format your response with appropriate markdown for readability
    5. Use examples and analogies to clarify complex concepts
    6. Avoid jargon and overly technical language unless necessary
    
    LEARNING STYLE ADAPTATIONS:
    - For Visual learners: Include descriptions of visual concepts, diagrams, or mental models
    - For Text-based learners: Provide clear, structured explanations with defined concepts
    - For Hands-on learners: Include practical examples, exercises, or applications

    Your explaination should be educational, accurate and engaging.
    """
    return prompt
