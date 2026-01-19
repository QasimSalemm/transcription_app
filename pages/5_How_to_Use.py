import os
import streamlit as st

def how_to_use_page():
    # Find image path relative to this file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    icon_path = os.path.join(parent_dir, "Images", "voice.png")

    st.set_page_config(
        page_title="How to Use - Speech to Text App", 
        layout="wide",
        page_icon=icon_path
        )

    # Page Title
    st.title("How to Use")

    st.write(
        "Follow these simple steps to get started with the Speech-to-Text Transcription App."
    )

    # Step 1
    st.header("Step 1: Upload Your File")
    st.write(
        "Click the **Upload Audio/Video File** button on the main page. "
        "You can upload common formats such as MP3, WAV, MP4, AVI, and more."
    )

    # Step 2
    st.header("Step 2: Choose Settings")
    st.write(
        "Select your preferred **model size** (tiny, base, small, medium, large). "
        "You can also select a **language option**, choose to include **word-level timestamps**, "
        "and set an optional **chunk size** to split long transcripts."
    )

    # Step 3
    st.header("Step 3: Start Transcription")
    st.write(
        "Click the **Start Transcription** button. "
        "The app will process your file and show a live progress bar during transcription."
    )

    # Step 4
    st.header("Step 4: Review Your Transcript")
    st.write(
        "When transcription is complete, the results will appear in a table. "
        "You can scroll through, check timestamps, and review the text."
    )

    # Step 5
    st.header("Step 5: Download the Transcript")
    st.write(
        "Click the **Download** button to save the transcript as a CSV file. "
        "The file name will include the date and time for easy reference."
    )

    # Step 6
    st.header("Step 6: Clear All (Optional)")
    st.write(
        "Click the **Clear All** button if you want to remove uploaded files and reset the session. "
        "This will also delete any temporary files created during transcription."
    )

    # Footer
    st.write("---")
    st.success("💡 Tip: For best results, use clear audio recordings with minimal background noise.")

if __name__ == "__main__":
    how_to_use_page()
