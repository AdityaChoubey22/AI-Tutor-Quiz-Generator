from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class TutoringRequest(BaseModel):
    subject: str = Field(..., description="Academic subject")
    level: str = Field(..., description="Learing Level(Begineer, Intermediate, Advanced)")
    question: str = Field(..., description="User's questions")
    learning_style: str = Field("Text-Based", description="Preferred Learning Style")
    background: str = Field("Unknown", description="User's background knowledge Level")
    language: str = Field("English", description="Preferred Language")

class QuizRequest(BaseModel):
    subject: str = Field(..., description="Academic subject")
    level: str = Field(..., description="Learning Level")
    num_questions: int = Field(5, description="Number of quiz questions", ge=1, le=100)
    reveal_answer: Optional[bool] = Field(True, description="Whether to format with hidden answers")


class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    correct_answer: str
    explanation: Optional[str] = None

class TutoringResponse(BaseModel):
    response: str

class QuizResponse(BaseModel):
    quiz: List[Dict[str, Any]]
    formatted_quiz: Optional[str] = None