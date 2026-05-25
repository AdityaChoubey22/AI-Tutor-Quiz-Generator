# AI Powered Tutor and Quiz Generator 🎓🤖

This project is an **AI-driven tutoring and quiz generation system** built using **FastAPI** for the backend and a customizable frontend. It leverages LLMs (like OpenAI or similar) to generate quizzes and tutoring explanations dynamically.

---

## 🚀 Features

- Generate quizzes on any topic via LLM
- Export quizzes in HTML format
- Tutor explanations for given topics
- Modular and well-organized Python codebase
- Easy to extend and integrate

---
## 🧰 Technologies Used

The project leverages the following technologies:

### 🔙 Backend
- **Python 3.12** – Core programming language
- **FastAPI** – High-performance web framework for building APIs
- **Uvicorn** – ASGI server to run FastAPI
- **Pydantic** – Data validation and parsing
- **dotenv** – Load environment variables from `.env` files
- **OpenAI API** – Used for AI-based tutoring and quiz generation
- **asyncio** – For handling asynchronous operations

### 🧪 Testing / Utilities

- **Custom Scripts** – For prompt generation, quiz formatting, etc.

### 🖼 Frontend (optional or extendable)
- Minimal frontend setup using Streamlit 

### 📁 Project Management
- **VS Code** – Recommended IDE
- **Git** – Version control
- **Markdown** – For documentation (`README.md`)

---

## ⚙️ Setup Instructions

### 1. 📦 Clone the Repository

```bash
git clone https://github.com/your-username/ai-powered-tutor-and-quiz-generator.git

cd ai-powered-tutor-and-quiz-generator
```
### 2. 📜 Install Dependencies

Ensure you have Python 3.10+ installed. Then install required packages:

```bash
pip install -r requirements.txt
```

### 3. 🔐 Set Up Environment Variables

Create a .env file in the root directory and define your environment variables. For example:

```bash
OPENAI_API_KEY = your-openai-api-key
MODEL_NAME = the-name-of-model
TEMPERATURE = temperature-of-model
```

### 4. 🏃 Run the Backend Server

Navigate to the backend directory and start the server using Uvicorn:

```bash
cd backend
uvicorn main:app --reload
```

### 5. 🏃 Run the Frontend Server

Navigate to the Frontend directory and run the frontend file(streamlit file):

```bash
streamlit run frontend.py
```

### 6. 🛠 Optional: Run Auto Folder Structure Script

If you want to automatically create the folder and file structure:

```bash
python structure.py
```
This script will create all folders and files defined in the structure dictionary inside structure.py.