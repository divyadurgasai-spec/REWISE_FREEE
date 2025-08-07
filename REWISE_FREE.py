import streamlit as st
import requests

# Streamlit page configuration
st.set_page_config(page_title="REWISE: Exam Prep Tool", page_icon="📚")

st.title("📚 REWISE: AI-Powered Exam Prep Tool")
st.markdown("Generate revision notes, MCQs, assertion-reason questions, mnemonics, diagrams, or summaries for **any exam or subject**.")

# User inputs
api_key = st.text_input("🔑 Enter your OpenRouter API Key (https://openrouter.ai/keys)", type="password")
exam = st.text_input("🎓 Enter Exam (e.g., NEET, JEE, CBSE)")
subject = st.text_input("📘 Enter Subject (e.g., Biology, Physics, Chemistry, Maths)")
topic = st.text_input("🔍 Enter Topic")
level = st.selectbox("📈 Select Difficulty Level", ["Beginner", "Intermediate", "Advanced"])
question_type = st.selectbox("❓ Question Type", ["MCQ", "Assertion-Reason", "Both"])
num_questions = st.slider("#️⃣ Number of Questions", 1, 20, 5)
output_format = st.selectbox("🗂 Export Format", ["Text", "PDF"])

# Output type
output_type = st.selectbox("🔧 What do you want to generate?", [
    "Revision Notes",
    "Mnemonics",
    "MCQs",
    "Assertion-Reason Questions",
    "Diagram Description",
    "Tabular Summary"
])

# Model selector
model = st.selectbox("🧠 Choose a Model", [
    "mistralai/mixtral-8x7b", 
    "meta-llama/llama-3-8b-instruct", 
    "google/gemma-7b-it"
])

if st.button("⚡ Generate"):
    if not api_key or not topic or not subject or not exam:
        st.warning("Please fill in all required fields.")
    else:
        with st.spinner("Generating..."):
            # Create prompt based on user selection
            if output_type == "MCQs":
                user_prompt = f"Generate {num_questions} {question_type} questions with answers and explanations for {exam} {subject} on the topic '{topic}' at {level} level."
            else:
                prompt_map = {
                    "Revision Notes": f"Generate concise revision notes for {exam} {subject} on the topic '{topic}' at {level} level.",
                    "Mnemonics": f"Create helpful mnemonics for key concepts in {exam} {subject} - Topic: {topic}.",
                    "Assertion-Reason Questions": f"Generate {num_questions} assertion-reason questions with explanations for {exam} {subject} - Topic: {topic}.",
                    "Diagram Description": f"Describe the important biological/physics/chemistry diagram for the topic '{topic}' from {subject}. Include key labels and explanations.",
                    "Tabular Summary": f"Summarize key concepts in {subject} - Topic: {topic} in a table with headings like Concept, Explanation, and Examples."
                }
                user_prompt = prompt_map.get(output_type, "")

            headers = {
                "Authorization": f"Bearer {api_key}",
                "HTTP-Referer": "rewise-free.streamlit.app",
                "X-Title": "REWISE Multisubject"
            }

            data = {
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are an expert tutor helping students with {exam} {subject}."},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.7
            }

            response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

            if response.status_code == 200:
                output_text = response.json()["choices"][0]["message"]["content"]
                st.success("✅ Done!")
                st.markdown(f"### 📄 {output_type} for **{topic} ({subject})**")
                st.markdown(output_text)
            else:
                st.error(f"❌ Error: {response.status_code} - {response.json()}")
