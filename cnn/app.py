

import os

import streamlit as st
from dotenv import load_dotenv

from services.ai_service import AIServiceError, generate_reply


load_dotenv()

st.set_page_config(page_title="AI Assistant", page_icon="AI", layout="centered")
st.title("AI Assistant")
st.caption("A simple Streamlit chatbot powered by OpenAI.")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("Controls")
    model_name = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    st.caption(f"Model: `{model_name}`")
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    if os.getenv("OPENAI_API_KEY"):
        st.success("API key configured")
    else:
        st.warning("Add `OPENAI_API_KEY` to `.env` before sending a message.")

if not st.session_state.messages:
    st.info("Start a conversation by asking a question below.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask me anything")
if prompt:
    prompt = prompt.strip()
    if not prompt:
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                reply = generate_reply(st.session_state.messages)
            except AIServiceError as error:
                reply = f"Warning: {error}"
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
