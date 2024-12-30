from dotenv import load_dotenv
import os
from openai import OpenAI
import streamlit as st
load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


MODEL = 'gpt-4o-mini'

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = MODEL



system_prompt = """
You are helpfull assistant. Helping building AI agents using python, vector base. 

if user not asking for any framework soluton (langchain, crewAi, etc.) provide using pure pyton only with modules like openai, google gemini or etc.
"""




st.title("AI Chat")

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role":"user","content": prompt})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        st.session_state.messages.append({"role": "system", "content": system_prompt})
        stream = client.chat.completions.create(
        model = st.session_state["openai_model"],
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True
    )
    response = st.write_stream(stream)
    st.session_state.messages.append({"role":"assistant", "content":response})