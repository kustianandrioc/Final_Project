%%writefile streamlit_chat_app.py

import streamlit as st
from google import genai

st.title("Chatbot Umum")
st.caption("ChatBot Umum")

with st.sidebar:
    st.subheader("Pengaturan")

    google_api_key = st.text_input("Google AI API Key", type="password")

    reset_button = st.button("Hapus Percakapan", help="Hapus semua pesan dan mulai dari awal")

if not google_api_key:
    st.info("Masukkan Google AI API Key di sidebar untuk mulai chat.", icon="🗝️")

    st.stop()

if ("genai_client" not in st.session_state) or (
    getattr(st.session_state, "_last_key", None) != google_api_key
):
    try:
        st.session_state.genai_client = genai.Client(api_key=google_api_key)

        st.session_state._last_key = google_api_key

        st.session_state.pop("chat", None)
        st.session_state.pop("messages", None)

    except Exception as e:
        st.error(f"API Key tidak valid: {e}")
        st.stop()

if "chat" not in st.session_state:

    st.session_state.chat = st.session_state.genai_client.chats.create(
        model="gemini-3.5-flash"
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

if reset_button:
    st.session_state.pop("chat", None)
    st.session_state.pop("messages", None)

    st.rerun()

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Ketik pesanmu di sini...")


if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        response = st.session_state.chat.send_message(prompt)

        if hasattr(response, "text"):
            answer = response.text
        else:
            answer = str(response)

    except Exception as e:
        answer = f"Terjadi error: {e}"

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
