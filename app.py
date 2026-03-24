import streamlit as st
import google.generativeai as genai
import csv

def load_customer_data(file_path):
    table_header = "| customer_name | customer_machine | no_of_files |\n| :--- | :--- | :--- |\n"
    table_rows = ""
    
    try:
        with open(file_path, mode='r', encoding='utf-8-sig') as f: # 'utf-8-sig' handles Excel BOM
            reader = csv.DictReader(f)
            # Clean the headers (removes accidental spaces)
            reader.fieldnames = [name.strip() for name in reader.fieldnames]
            
            for row in reader:
                table_rows += f"| {row['customer_name']} | {row['customer_machine']} | {row['no_of_files']} |\n"
        
        return f"### CUSTOMER DATA\n\n{table_header}{table_rows}"
    except KeyError as e:
        return f"Error: Column {e} not found in CSV. Check your headers!"

lesson_text = load_customer_data("customers.csv")

class Bot:
    def __init__(self, api_key, lesson_content):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash-lite')
        self.lesson_data = lesson_content

        self.system_instruction = (
            "You are a professional PMI Instructor. "
            "Answer questions based ONLY on the provided lesson context. "
            "If the answer isn't in the context, say you don't know."
        )

    def ask_question(self, user_query):
        prompt = f"""
{self.system_instruction}

CONTEXT FROM LESSON:
{self.lesson_data}

USER QUESTION:
{user_query}
"""
        response = self.model.generate_content(prompt)
        return response.text


st.set_page_config(page_title="Project Management Chatbot", layout="centered")

st.title("Project Management Chatbot")
st.write("Ask questions based on the lesson content")

api_key = st.secrets["GEMINI_API_KEY"]

if api_key:
    bot = Bot(api_key, lesson_text)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask your question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        answer = bot.ask_question(prompt)

        st.session_state.messages.append({"role": "assistant", "content": answer})

        with st.chat_message("assistant"):
            st.markdown(answer)

else:
    st.warning("Please enter your API key to start.")
