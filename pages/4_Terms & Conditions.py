import streamlit as st

def terms_page():
    st.set_page_config(
        page_title="Terms & Conditions - Speech to Text App", 
        layout="wide",
        page_icon="🎙️"
        )

    # Page Title
    st.title("Terms & Conditions")

    st.write(
        "By using the Speech-to-Text Transcription App, you agree to the following Terms & Conditions. "
        "Please read them carefully before using the service."
    )

    st.header("1. Acceptance of Terms")
    st.write(
        "By accessing or using this app, you agree to be bound by these Terms & Conditions. "
        "If you do not agree, you should not use the app."
    )

    st.header("2. Use of the Service")
    st.write(
        "The app is provided for personal, educational, and research purposes. "
        "You agree not to misuse the app, including attempting to reverse engineer, copy, or resell it."
    )

    st.header("3. User Content")
    st.write(
        "You are responsible for the content you upload. "
        "Please ensure that you have the rights to use any audio or video files submitted for transcription."
    )

    st.header("4. Data Handling")
    st.write(
        "Uploaded files are processed locally during your session. "
        "We do not permanently store, share, or sell your data. "
        "Temporary files are deleted when you clear the session."
    )

    st.header("5. Intellectual Property")
    st.write(
        "The underlying code, design, and features of this app are the intellectual property of the developers. "
        "You may not reproduce or distribute them without permission."
    )

    st.header("6. Disclaimer of Warranty")
    st.write(
        "This app is provided 'as is' without warranties of any kind. "
        "We do not guarantee uninterrupted service, error-free transcription, or complete accuracy."
    )

    st.header("7. Limitation of Liability")
    st.write(
        "We shall not be liable for any direct, indirect, incidental, or consequential damages "
        "arising from your use of the app."
    )

    st.header("8. Modifications to Terms")
    st.write(
        "We reserve the right to update these Terms & Conditions at any time. "
        "Continued use of the app after changes constitutes acceptance of the updated terms."
    )

    # Footer
    st.write("---")
    st.info("📌 If you have questions about these Terms & Conditions, please contact us at qasimsaleem317@gmail.com")

if __name__ == "__main__":
    terms_page()
