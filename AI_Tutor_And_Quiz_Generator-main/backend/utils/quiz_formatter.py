def format_quiz_for_reveal(quiz_data):
    """
    Format quiz data into HTML with hidden answers that can be revealed on click.

    Args:
        quiz_data (list): List of question dictionaries

    Returns:
        str: HTML string with quiz questions and hidden answers
    """
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            html, body {
                height: 100%;
                margin: 0;
                padding: 0;
            }
            body{
                font-family: Arial, Helvetica, sans-serif;
                color: white;
                background-color: #121212;
                overflow-y: auto;
            }
            .quiz-container{
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            .question{
                margin-bottom: 30px;
                padding: 20px;
                border: 1px solid #444;
                border-radius: 10px;
                background-color: #1e1e2f;
            }
            .question h3{
                margin-top: 0;
                color: #90caf9;
            }
            .option{
                margin: 10px 0;
                padding: 12px;
                border: 1px solid #555;
                border-radius: 6px;
                background-color: #2d2d44;
                transition: background-color 0.2s;
            }
            .option:hover{
                background-color: #3a3a5a;
            }
            .reveal-btn{
                background-color: #2196f3;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
            }
            .reveal-btn:hover{
                background-color: #0d8bf2;
            }
            .answer-section{
                margin-top: 20px;
                border: 2px solid #ffeb3b;
                border-radius: 8px;
                padding: 0;
                overflow: hidden;
                display: none;
            }
            .answer-header{
                background-color: #ffeb3b;
                color: #000;
                padding: 10px;
                font-weight: bold;
                font-size: 16px;
                text-align: center;
            }
            .answer-content{
                padding: 15px;
                background-color: #1a237e;
            }   
            .correct-answer{
                font-size: 18px;
                font-weight: bold;
                color: white;
                margin-bottom: 15px;
            }
            .explanation{
                color: #e1f5fe;
                font-size: 16px;
                line-height: 1.5;
            }
            .selected-correct{
                background-color: #1b5e20 !important;
                border-color: #4caf50 !important;
            }
            .selected-incorrect{
                background-color: #b71c1c !important;
                border-color: #f44336 !important;
            }
        </style>
        <title>Document</title>
    </head>
    <body>
        <div class="quiz-container">
            <h2 style="color: #2196f3; text-align: center; margin-bottom: 30px;">Interactive Quiz</h2>
        """
    for i, question in enumerate(quiz_data,1):
        option_letters = ["A", "B", "C", "D"]
        correct_index = question["options"].index(question["correct_answer"]) if question["correct_answer"] in question["options"] else 0
        html += f"""
        <div class="question" id="question-{i}">
            <h3>Question {i}</h3>
            <p>{question["question"]}</p>
            <div class="options">
        """
        for j, option in enumerate(question["options"]):
            is_correct = "true" if j == correct_index else "false"
            html += f"""
            <div class="option" id="option-{i}-{j}" onclick="selectOption({i}, {j}, {is_correct})">
                <strong>{option_letters[j]}.</strong> {option}
            </div>
        """
        
        html += f"""
            </div>
            <button class="reveal-btn" onclick="revealAnswer({i})">Show Answer</button>
            <div class="answer-section" id="answer-{i}">
                <div class="answer-header">Correct Answer</div>
                <div class="answer-content">
                    <div class="correct-answer">{option_letters[correct_index]}. {question["correct_answer"]}</div>
                    <div class="explanation">{question.get("explanation","")}</div>
                </div>
            </div>
        </div>
        """
    html += """
    </div>
    <script>
        function selectOption(questionNumber, optionNumber, isCorrect) {
            const questionId = `question-${questionNumber}`;
            const options = document.querySelectorAll(`#${questionId} .option`);
            options.forEach(option => {
                option.className = 'option';
            });
            const selectedOption = document.getElementById(`option-${questionNumber}-${optionNumber}`);
            if(isCorrect) {
                selectedOption.className = 'option selected-correct';
            } else {
                selectedOption.className = 'option selected-incorrect';
                revealAnswer(questionNumber);
            }
        }
        function revealAnswer(questionNumber) {
            const answerDiv = document.getElementById(`answer-${questionNumber}`);
            answerDiv.style.display = 'block';
            setTimeout(() => {
                answerDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }, 100);
            answerDiv.animate([
                {transform:'scale(1)', boxShadow: '0 0 0 rgba(255,235,59,0)'},
                {transform:'scale(1.03)', boxShadow: '0 0 20px rgba(255,235,59,0.7)'},
                {transform:'scale(1)', boxShadow: '0 0 10px rgba(255,235,59,0.3)'},
            ], {
                duration: 1000,
                iterations: 1,
            });     
        }
    </script>
</body>
</html>
"""
    return html