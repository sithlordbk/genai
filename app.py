import streamlit as st
import google.generativeai as genai

lesson_text = """
customer_name,customer_machine,no_of_files
ABC,MachineA,100
XYZ,MachineC,250
LMN,MachineB,500
"""

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
