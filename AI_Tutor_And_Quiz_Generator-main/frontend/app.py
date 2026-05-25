import streamlit as st
import requests
import uuid
import random
from streamlit.components.v1 import html

# Page Configuration
st.set_page_config(page_title="AI Tutor", layout="wide")

# App Title
st.title("AI-Powered Tutor & Quiz App")

# creating side navigation bar
with st.sidebar:
    st.header("Learning Prefrences")
    subject = st.selectbox("📘 Select Subject", 
                        ["Mathematics", "Physics", "Computer Science", 
                        "History", "Biology", "Programming"])
    level = st.selectbox("📚 Select Learning Level", 
                    ["Beginner", "Intermediate", "Advanced"])
    learning_style = st.selectbox("🎓 Learning Style", 
                                ["Visual", "Text-based", "Hands-on"])
    language = st.selectbox("🌍 Preferred Language", 
                            ["English", "Hindi", "Spanish", "French"])
    background = st.selectbox("📊 Background Knowledge", 
                            ["Beginner", "Some Knowledge", "Experienced"])

# API endpoint for local backend
API_ENDPOINT = "http://127.0.0.1:8000"

tab1, tab2 = st.tabs(["✍️ Ask A Question","📊 Take A Quiz"])

# -------------------- TAB 1: Tutor --------------------
with tab1:
    st.header("Ask Your Question")
    question = st.text_area("❓ What Do You Like To Learn Today?","Explain Newton's Second Law Of Motion")

    if st.button("Get Explaination 🧠"):
        with st.spinner("Generating Personalized Explaination..."):
            try:
                response = requests.post(f"{API_ENDPOINT}/tutor",
                            json={
                                "subject":subject,
                                "level":level,
                                "learning_style":learning_style,
                                "language":language,
                                "background":background,
                                "question":question
                            }).json()
                st.success("Here is your personalized explaination:")
                st.markdown(response["response"],unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error getting explaination: {str(e)}")
                st.info(f"Make sure the backend server is running at {API_ENDPOINT}")

# -------------------- TAB 2: Quiz --------------------
with tab2:
    st.header("Test Your Knowledge")
    
    # Text input box for the custom quiz topic
    quiz_topic = st.text_input(
        "📝 Enter Quiz Topic:", 
        value=subject, 
        placeholder="e.g., Quantum Physics, Calculus, Python Loops, French Vocabulary..."
    )
    
    col1, col2 = st.columns([2,1])
    with col1:
        num_questions = st.selectbox(
            "Number Of Questions",
            options=list(range(1, 101)),
            index=4
        )
    with col2:
        # Align button vertically with the slider
        st.write("##")
        quiz_button = st.button("Generate Quiz ✍️",use_container_width=True)
    if quiz_button:
        with st.spinner("Creating Quiz Questions..."):
            try:
                response = requests.post(
                        f"{API_ENDPOINT}/quiz",
                        json={
                            "subject": quiz_topic if quiz_topic else subject,
                            "level":level,
                            "num_questions":num_questions,
                            "reveal_answer":True
                        }
                    ).json()
                st.success("Quiz generated! Try Answering These Questions...")
                if "formatted_quiz" in response and response["formatted_quiz"]:
                    html(response["formatted_quiz"], height=800, scrolling=True)
                else:
                    for i,q in enumerate(response["quiz"]):
                        with st.expander(f"Question {i+1}: {q['question']}",expanded=True):
                            session_id = str(uuid.uuid4())
                        
                        selected = st.radio(
                            "Select Your Answers:",
                            q["options"],
                            key = f"q_{session_id}"
                        )
                        if st.button("Check Answer",key=f"check_{session_id}"):
                            if selected == q["correct_answer"]:
                                st.success(f"✅ Correct! {q.get('explanation','')}")
                            else:
                                st.error(f"❌ Incorrect. The correct answer is: {q['correct_answer']}")
                                if "explanation" in q:
                                    st.info(q["explanation"])
            except Exception as e:
                st.error(f"Error generating quiz: {str(e)}")
                st.info(f"Make sure the backend server is running at {API_ENDPOINT}")

# Footer
st.markdown("---")
st.markdown("⚡ Powered by AI - Your Personal Learning Assistant")
