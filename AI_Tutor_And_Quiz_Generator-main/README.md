
<p align="center">
  <h1 align="center">🎓 AI Tutor & Quiz Generator</h1>
  <p align="center">
    Personalized AI tutoring and dynamic multiple-choice quizzes — built with FastAPI & Streamlit.
  </p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/LangChain-1C3C3C?logo=langchain&logoColor=white" alt="LangChain"/>
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License"/>
</p>

---

## ✨ What is this?

**AI Tutor & Quiz Generator** is a full-stack learning app that helps students study smarter:

- **Ask a question** — get a tailored explanation based on subject, level, learning style, language, and background.
- **Take a quiz** — generate 1–100 multiple-choice questions on any topic, with instant answer reveal and explanations.

The backend orchestrates multiple LLM providers with automatic fallback; the frontend delivers a clean, interactive Streamlit experience.

---

## 🚀 Features

| Feature | Description |
|--------|-------------|
| 🧠 **AI Tutor** | Step-by-step explanations adapted to your learning preferences |
| 📝 **Smart Quizzes** | MCQs with 4 options, correct answers, and explanations |
| 🎯 **Custom Topics** | Quiz on any subject or custom topic (e.g. *Python Loops*, *Quantum Physics*) |
| 📊 **Difficulty Levels** | Beginner · Intermediate · Advanced |
| 🌍 **Multi-language** | English, Hindi, Spanish, French |
| 🔄 **Provider Rotation** | OpenRouter → Hugging Face → Gemini → keyless Pollinations fallback |
| 📤 **HTML Export** | Interactive quiz UI via `/quiz_html` endpoint |
| ⚡ **Batch Generation** | Efficient chunked quiz creation for large question sets |

---

## 🏗 Architecture
┌─────────────────────┐ HTTP ┌─────────────────────┐ │ Streamlit UI │ ──────────────────► │ FastAPI Backend │ │ frontend/app.py │ /tutor, /quiz │ backend/main.py │ └─────────────────────┘ └──────────┬──────────┘ │ ▼ ┌─────────────────────┐ │ LLM Layer │ │ OpenRouter / HF / │ │ Gemini / Pollinations│ └─────────────────────┘



---

## 🛠 Tech Stack

**Backend:** Python · FastAPI · Uvicorn · Pydantic · LangChain · python-dotenv  

**Frontend:** Streamlit  

**AI:** OpenRouter · Google Gemini · Hugging Face · Pollinations.ai (no key)

---

## 📁 Project Structure
AI_Tutor_And_Quiz_Generator/ ├── backend/ │ ├── main.py # API routes │ ├── llm_invoke/llm.py # Multi-provider LLM with rotation │ ├── services/ │ │ ├── quiz_service.py # Quiz generation logic │ │ └── tutor_service.py # Tutoring logic │ ├── validation/ # Parsing & fallback handling │ ├── utils/ # Prompts & HTML formatting │ └── .env # API keys (not committed) ├── frontend/ │ └── app.py # Streamlit UI ├── requirements.txt └── README.md



---
## ⚙️ Getting Started
### Prerequisites
- Python **3.10+**
- pip
- A free API key from one of: [OpenRouter](https://openrouter.ai/keys) · [Google AI Studio](https://aistudio.google.com/app/apikey) · [Hugging Face](https://huggingface.co/settings/tokens)  
  *(Or run keyless via Pollinations — slower and less reliable.)*

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/AI_Tutor_And_Quiz_Generator.git
cd AI_Tutor_And_Quiz_Generator
2. Install dependencies
pip install -r requirements.txt
3. Configure environment variables
Create backend/.env:

# OpenRouter (recommended)
OPENROUTER_API_KEY_1=your_openrouter_key_here
OPENROUTER_MODEL=meta-llama/llama-3.3-70b-instruct:free
# Optional — add more providers
# GEMINI_API_KEY_1=your_gemini_key_here
# HUGGINGFACE_API_KEY_1=your_hf_key_here
TEMPERATURE=0.7
⚠️ Never commit .env to Git. It is already listed in .gitignore.

4. Run the backend
cd backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
API docs: http://127.0.0.1:8000/docs

5. Run the frontend
In a new terminal:

cd frontend
streamlit run app.py
Open: http://localhost:8501

📡 API Endpoints
Method	Endpoint	Description
GET
/health
Health check
POST
/tutor
Personalized tutoring response
POST
/quiz
Generate quiz (JSON + optional HTML)
GET
/quiz_html/{subject}/{level}/{num_questions}
Standalone HTML quiz page
Example — Tutor

curl -X POST http://127.0.0.1:8000/tutor \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Physics",
    "level": "Beginner",
    "question": "Explain Newton'\''s second law",
    "learning_style": "Visual",
    "background": "Beginner",
    "language": "English"
  }'
Example — Quiz

curl -X POST http://127.0.0.1:8000/quiz \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Mathematics",
    "level": "Beginner",
    "num_questions": 5,
    "reveal_answer": true
  }'
🖥 Screenshots
Add screenshots of the Tutor tab and Quiz tab after running the app.

☁️ Deployment (Free)
Component	Suggested platform
Backend (FastAPI)
Render · Railway · Fly.io
Frontend (Streamlit)
Streamlit Community Cloud
Update API_ENDPOINT in frontend/app.py to your deployed backend URL before going live.

🐛 Troubleshooting
Issue	Fix
"Sample … question #1" placeholders
Invalid/expired API key or model ID — check backend/.env and backend logs
Connection error in Streamlit
Ensure backend is running on port 8000
Slow quiz generation
Free-tier rate limits; try a Gemini key or fewer questions
429 rate limit
App auto-rotates keys; add another provider key or wait and retry
🤝 Contributing
Contributions are welcome! Feel free to open issues or submit pull requests for:

UI/UX improvements
New LLM providers
Better quiz parsing
Deployment configs
📄 License
This project is open source under the MIT License — see LICENSE for details.

🙏 Acknowledgments
Built with FastAPI, Streamlit, and LangChain.

Made with ❤️ for learners everywhere
