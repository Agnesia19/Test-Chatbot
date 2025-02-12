import streamlit as st
from hugchat import hugchat
from hugchat.login import Login

st.title("💬 HugChat Indonesia")

# Inisialisasi session state untuk menyimpan pesan
if "messages" not in st.session_state:
    st.session_state.messages = []

# Form input untuk login
st.sidebar.title("📧 Login HugChat")
st.sidebar.markdown("Masukkan akun HuggingFace Anda")

hf_email = st.sidebar.text_input("Masukkan Email:", type="default")
hf_pass = st.sidebar.text_input("Masukkan Password:", type="password")

if st.sidebar.button("👉 Mulai Chat", type="primary"):
    st.session_state.messages = []
    st.sidebar.success("Berhasil Login!")

def generate_response(prompt_input, email, passwd):
    try:
        # Tambahkan instruksi untuk bahasa Indonesia
        modified_prompt = f"Tolong jawab dalam Bahasa Indonesia: {prompt_input}"
        
        sign = Login(email, passwd)
        cookies = sign.login()
        chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
        
        # Set default ke Bahasa Indonesia
        chatbot.chat("Mulai sekarang, jawab semua pertanyaan dalam Bahasa Indonesia dengan gaya yang natural dan ramah.")
        
        return chatbot.chat(modified_prompt)
    except Exception as e:
        return f"Terjadi kesalahan: {str(e)}"

# Area chat
st.write("💡 Ketik pesan Anda di bawah ini")

# User input
if prompt := st.chat_input("Ketik pesan Anda..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Generate response
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Sedang berpikir..."):
                response = generate_response(prompt, hf_email, hf_pass)
                st.write(response)
                
        message = {"role": "assistant", "content": response}
        st.session_state.messages.append(message)

# Tampilkan riwayat chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Informasi tambahan
st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ Informasi")
st.sidebar.markdown("""
- Chat ini menggunakan model HuggingFace
- Diperlukan akun HuggingFace untuk menggunakan layanan ini
- Semua jawaban dalam Bahasa Indonesia
""")
