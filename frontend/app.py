import streamlit as st
import requests

st.title("Personal AI Voice Agent")
st.caption("Phase 1: Text chat (voice coming soon)")

BACKEND_URL = "http://localhost:8000/chat"

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Ask me anything...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = requests.post(BACKEND_URL, json={"message": user_input})
            reply = response.json()["reply"]
            st.write(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})