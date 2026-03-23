import streamlit as st
import google.generativeai as genai
import os

# --- LESSON CONTENT ---
lesson_text = """
1. PROJECTS VS. OPERATIONS:
   - Project: A temporary endeavor with a unique result, product, or service.
   - Operations: Ongoing, repetitive work to maintain a business or service (e.g., server maintenance).

2. ORGANIZATIONAL STRUCTURES:
   - Functional: Managed by a functional manager; team members report only to them.
   - Project-Oriented: The Project Manager (PM) has full authority over the budget and team.
   - Matrix (Weak, Balanced, Strong): A mix where power is shared between PMs and functional managers.
     * Strong Matrix: PM has more authority.
     * Weak Matrix: Functional manager has more authority.

3. ENTERPRISE ENVIRONMENTAL FACTORS (EEFs):
   - Internal/External conditions, not under the project's control, that influence the project.
   - Internal EEFs: Infrastructure (servers), IT software (OS, APIs), Resource availability.
   - External EEFs: Marketplace conditions, legal restrictions, social/cultural influences.

4. ORGANIZATIONAL PROCESS ASSETS (OPAs):
   - Plans, processes, policies, and knowledge bases specific to the performing organization.
   - Examples: Standardized templates, historical data, lessons learned repositories, security policies.

5. PROJECT MANAGEMENT OFFICE (PMO):
   - Supportive: Provides templates and best practices (low control).
   - Controlling: Requires compliance with frameworks (moderate control).
   - Directive: Manages the project directly (high control).

6. PROGRAMS AND PORTFOLIOS:
   - Program: A group of related projects managed together to achieve common benefits.
   - Portfolio: A collection of projects, programs, and operations managed as a group to achieve strategic objectives.
"""

# --- BOT CLASS ---
class Bot:
    def __init__(self, api_key, lesson_content):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-3-flash-preview')
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


# --- STREAMLIT UI ---
st.set_page_config(page_title="PMI Lesson Chatbot", layout="centered")

st.title("📘 Project Management Lesson Chatbot")
st.write("Ask questions based on the lesson content")

api_key = st.secrets["GEMINI_API_KEY"]

if api_key:
    bot = Bot(api_key, lesson_text)

    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User input
    if prompt := st.chat_input("Ask your question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        # Get response
        answer = bot.ask_question(prompt)

        st.session_state.messages.append({"role": "assistant", "content": answer})

        with st.chat_message("assistant"):
            st.markdown(answer)

else:
    st.warning("Please enter your API key to start.")
