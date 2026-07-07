import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# === Konfigurasi dasar aplikasi ===
st.set_page_config(page_title="Han&", page_icon="💬", layout="centered")

# Custem CSS
st.markdown("""
            <style>
            /* Chat bubble untuk pengguna */
            .user-bubble {
            background-color: #E3F2FD;
            color: #0D47A1;
            padding: 10px;
            border-radius: 12px;
            margin: 5px 0;
            display: inline-block;
            max-width: 80%;
            float: right;
            clear: both;
            }

            /* Chat bubble untuk bot */
            .bot-bubble {
                background-color: #BBDEFB;
                color: #0D47A1;
                padding: 10px;
                border-radius: 12px;
                margin: 5px 0;
                display: inline-block;
                max-width: 80%;
                float: left;
                clear: both;
            }

            /* Tombol reset */
            .stButton>button {
                background-color: #42A5F5;
                color: white;
                border-radius: 8px;
                padding: 8px 16px;
                transition: 0.3s;
            }

            .stButton>button:hover {
                background-color: #1E88E5;
            }
            </style>
            """, unsafe_allow_html=True)

# Judul aplikasi
st.markdown("<h2 style='text-align:center; sans-serif;'>💬 Tanya pada Han& </h2>", unsafe_allow_html=True)

# Simpan riwayat chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Fungsi untuk memanggil model Gemini
def ask_gemini(prompt):
    try:
        system_prompt = (
            "Kamu adalah Han&. "
            "Jawablah dengan bahasa sederhana, singkat, jelas, dan mudah dipahami. "
            "Gunakan kalimat pendek dan hindari istilah rumit. "
        )
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(system_prompt + "\n\nPertanyaan pengguna: " + prompt)
        return response.text.strip()
    except Exception as e:
        return f"Terjadi kesalahan: {e}"

# Input pengguna
user_input = st.chat_input("Tulis pertanyaan Anda...")

# Proses input pengguna
if user_input:
    # Tambahkan pertanyaan pengguna
    st.session_state.chat_history.append({"role": "user", "text": user_input})

    # Dapatkan jawaban dari Gemini
    with st.spinner("Han& sedang menjawab..."):
        bot_reply = ask_gemini(user_input)
        st.session_state.chat_history.append({"role": "bot", "text": bot_reply})

# === Tampilkan percakapan ===
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.markdown(f"<div class='user-bubble'>{chat['text']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-bubble'>{chat['text']}</div>", unsafe_allow_html=True)

# Tombol reset
if st.button("🔄 Reset Percakapan"):
    st.session_state.chat_history = []
    st.rerun()
