import streamlit as st
import requests

# Streamlit page config
st.set_page_config(page_title="REWISE: Notes Generator", page_icon="🧠")

st.title("🧠 REWISE: AI-Powered Revision Tool")
st.markdown("Generate NEET OR JEE -style notes, mnemonics, MCQs, or diagrams — for **any Biology topic**!")

# Input
note_prompt = st.text_input("📘 Enter your topic (e.g. DNA replication, photosynthesis)")
exam = input("Enter Exam (e.g., NEET/CBSE): ")
subject = input("Enter Subject (e.g., Biology): ")
topic = input("Enter Topic: ")
level = input("Enter Level (Beginner/Intermediate/Advanced): ")
num_questions = int(input("How many questions to generate? "))
question_type = input("Question Type (MCQ / Assertion-Reason): ")
output_format = input("Export format (txt / pdf): ")

# Options for what to generate
output_type = st.selectbox("🔧 What do you want to generate?", [
    "Revision Notes",
    "Mnemonics",
    "MCQs (Multiple Choice Questions)",
    "Diagram Description",
    "Tabular Summary"
])

# Model Selector
model = st.selectbox("🧠 Choose a Model", [ 
    "meta-llama/llama-3-8b-instruct",
])

# Button
if st.button("⚡ Generate"):
    
    else:
        with st.spinner("Generating..."):

            # Prompt mapping
            prompt_map = {
                "Revision Notes": f"Generate concise and NEET OR JEE-style revision notes on: {note_prompt}",
                "Mnemonics": f"Create creative mnemonics for remembering key concepts in: {note_prompt}",
                "MCQs (Multiple Choice Questions)": f"Generate 5 NEET OR JEE-style MCQs with answers and explanations for: {note_prompt}",
                "Diagram Description": f"Describe the biological diagram and key labels for: {note_prompt}",
                "Tabular Summary": f"Summarize key points from {note_prompt} in a table format (like concept vs detail)."
            }

            headers = {
                "HTTP-Referer": "rewise-free.streamlit.app",
                "X-Title": "REWISE Ultimate"
            }

            data = {
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are an expert NEEt&JEE tutor for SUBJECTS MATHS, PHYSICS, CHEMISTRY, BIOLOGY ."},
                    {"role": "user", "content": prompt_map[output_type]}
                ],
                "temperature": 0.7
            }

            response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

            if response.status_code == 200:
                notes = response.json()["choices"][0]["message"]["content"]
                st.success("✅ Done!")
                st.markdown(f"### 📝 {output_type} for **{note_prompt}**")
                st.markdown(notes)
            else:
                st.error(f"❌ Error: {response.status_code} - {response.json()}")

