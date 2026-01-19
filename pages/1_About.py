import streamlit as st

def about_page():
    st.set_page_config(
        page_title="About Us - Speech to Text App", 
        layout="wide",
        page_icon="🎙️"
        )

    # Page Title (H1)
    st.title("About Us")

    # Intro
    st.write(
        "Welcome to our **Speech-to-Text Transcription App**! "
        "We specialize in delivering fast, accurate, and easy-to-use transcription services "
        "powered by Faster-Whisper and Streamlit."
    )

    # Two-column layout
    col1, col2 = st.columns(2)

    with col1:
        st.header("Who We Are")
        st.write(
            "We are a team of developers and AI enthusiasts on a mission to make "
            "speech-to-text transcription simple and accessible. "
            "By leveraging advanced machine learning, we help users convert audio "
            "and video into accurate transcripts within seconds."
        )

        st.header("What We Offer")
        st.write("🎙️ Accurate Speech-to-Text")
        st.write("⏱️ Timestamps for words & segments")
        st.write("🌐 Multi-language support")
        st.write("📂 CSV Export")
        st.write("⚡ Fast & Lightweight Processing")

    with col2:
        st.header("Why Choose Us")
        st.write("✅ User-friendly interface")
        st.write("✅ Privacy first — your files stay local")
        st.write("✅ Supports multiple file formats (mp3, mp4, wav, etc.)")
        st.write("✅ Free to use, no signup required")

        st.header("Our Vision")
        st.write(
            "We believe that voice is the future of human-computer interaction. "
            "Our goal is to empower students, researchers, journalists, and creators "
            "by saving time on manual transcription."
        )

    # Footer
    st.write("---")
    st.info("💡 This project is open-source and community-driven. Contributions & feedback are always welcome!")

if __name__ == "__main__":
    about_page()
