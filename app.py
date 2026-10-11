import streamlit as st

st.set_page_config(
    page_title="VOICERA",
    page_icon="🎙️",
    layout="wide"
)

st.markdown("""
<style>
    .stApp {
        background: #f6f3ff;
    }

    .hero {
        background: linear-gradient(135deg, #8f7bd8, #b9a9ee);
        padding: 35px;
        border-radius: 25px;
        text-align: center;
        color: white;
        margin-bottom: 30px;
    }

    .hero h1 {
        font-size: 48px;
        margin: 0;
    }

    .hero p {
        font-size: 18px;
        margin-top: 8px;
    }

    .card {
        background: white;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 5px 20px rgba(80,60,130,0.08);
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>VOICERA</h1>
    <p>Your Voice, Your Word.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="card">
    <h2>🎙️ Speech-to-Text</h2>
    <p>Convert your voice into text directly from your browser.</p>
</div>
""", unsafe_allow_html=True)

audio = st.audio_input("🎤 Record your voice")

if audio:
    st.success("Audio recorded successfully!")
    st.audio(audio)
    st.info("Speech recognition will be connected in the next step.")

st.markdown("""
<div class="card">
    <h2>🔊 Text-to-Speech</h2>
    <p>Convert written text into natural speech.</p>
</div>
""", unsafe_allow_html=True)

text = st.text_area(
    "Enter text",
    placeholder="Type something here..."
)

if st.button("🔊 Speak"):
    if text.strip():
        st.info("Text-to-Speech will be connected in the next step.")
    else:
        st.warning("Please enter some text.")
