import streamlit as st

def privacy_policy_page():
    st.set_page_config(
        page_title="Privacy Policy - Speech to Text App", 
        layout="wide",
        page_icon="images/voice.png"
        )

    # Page Title (H1)
    st.title("Privacy Policy")

    st.write(
        "We value your privacy and are committed to protecting your personal data. "
        "This Privacy Policy explains how our Speech-to-Text Transcription App "
        "handles your information."
    )

    st.header("1. Data Collection")
    st.write(
        "Our app does not collect, store, or share your personal data. "
        "All audio and video files you upload remain on your local system "
        "and are processed directly within your session."
    )

    st.header("2. File Processing")
    st.write(
        "Uploaded audio and video files are used **only** for the purpose of transcription. "
        "We do not send your files to external servers or third-party services. "
        "Temporary files are automatically deleted when you clear or close the app."
    )

    st.header("3. Usage Information")
    st.write(
        "We may track general usage patterns (such as number of transcriptions performed) "
        "to improve app performance. This information is anonymized and cannot be linked "
        "to individual users."
    )

    st.header("4. Third-Party Services")
    st.write(
        "Our app relies on open-source tools such as Faster-Whisper and Streamlit. "
        "These libraries run locally and do not transmit your data externally."
    )

    st.header("5. Your Rights")
    st.write(
        "Since no personal data is stored, you do not need to request data deletion. "
        "However, you may clear uploaded files at any time using the 'Clear All' button."
    )

    st.header("6. Updates to This Policy")
    st.write(
        "We may update this Privacy Policy from time to time. "
        "Any changes will be reflected directly within this page."
    )

    st.write("---")
    st.info("📌 If you have any questions about this Privacy Policy, please contact us at qasimsaleem317@gmail.com")

if __name__ == "__main__":
    privacy_policy_page()
