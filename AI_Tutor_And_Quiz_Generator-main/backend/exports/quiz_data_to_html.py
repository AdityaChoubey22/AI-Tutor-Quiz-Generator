from utils.quiz_formatter import format_quiz_for_reveal
from config.logging import logger


def export_quiz_to_html(quiz_data, file_path = "quiz.html"):
    """
    Export the quiz data to an HTML file.

    Args:
        quiz_data (list): List of question dictionaries
        file_path (str): Path to save the HTML file
    """
    try:
        html_content = format_quiz_for_reveal(quiz_data)
        with open(file_path, 'w', encoding="utf-8") as f:
            f.write(html_content)
        logger.info(f"Quiz exported successfully to {file_path}")
        return True
    except Exception as e:
        logger.error(f"Error exporting quiz to HTML: {str(e)}")
        return False
