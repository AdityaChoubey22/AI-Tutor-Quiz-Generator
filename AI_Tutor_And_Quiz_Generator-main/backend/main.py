from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from fastapi.responses import HTMLResponse
import os
from dotenv import load_dotenv
import traceback
from models.request_response_model import QuizRequest, QuizResponse, TutoringRequest, TutoringResponse
from services.quiz_service import generate_quiz
from services.tutor_service import generate_tutoring_response

# Load environment variables from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize FastAPI app
app = FastAPI(
    title = "AI Quiz Grnerating and Tutoring App",
    discription = "An AI-powered tutoring and quiz generating application.",
    version = "1.0.0"
)

# creating the endpoints for the tutoring and quiz generating
@app.post("/tutor", response_model=TutoringResponse)
async def get_tutoring_response(data: TutoringRequest):
    """
    Generate a personalized tutoring response based on user input/ prefrences.
    """
    try:
        explanation = generate_tutoring_response(
            data.subject,
            data.level,
            data.question,
            data.learning_style,
            data.background,
            data.language
        )
        return {"response": explanation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating explanation: {str(e)}")

# endpoint for generating quiz
@app.post("/quiz", response_model=QuizResponse)
async def create_quiz(data: QuizRequest):
    """ 
    Generate a quiz based on the subject, level, and number of questions.
    """
    try:
        quiz_result = generate_quiz(
            data.subject,
            data.level,
            data.num_questions,
            reveal_answer=data.reveal_answer
        )

        if data.reveal_answer:
            return {
                "quiz": quiz_result["quiz_data"],
                "formatted_quiz": quiz_result["formatted_quiz"]
            }
        else:
            return {"quiz": quiz_result["quiz_data"]}
    except Exception as e:
        print("Error during /quiz:", traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error generating quiz: {str(e)}")


# creating the html endpoint for response saving
@app.get("/quiz_html/{subject}/{level}/{num_questions}",response_class=HTMLResponse)
async def get_quiz_html(subject: str, level: str, num_questions: int = 5):
    """
    Generate a quiz based on the subject, level, and number of questions.
    """
    try:
        quiz_result = generate_quiz(subject, level, num_questions, reveal_answer = True)
        return quiz_result["formatted_quiz"]
    except Exception as e:
        raise HTMLResponse(status_code=500, detail= f"Error Generating Quiz HTML: {str(e)}")

# Health status checking endpoint 
@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the server is running.
    """
    return {"status": "OK"}
