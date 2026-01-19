import datetime
import os
import tempfile
import time
import pandas as pd
import streamlit as st
try:
    from moviepy.editor import AudioFileClip, VideoFileClip
except ImportError:
    from moviepy import AudioFileClip, VideoFileClip
from faster_whisper import WhisperModel
import toml
import streamlit_logger as sl
import languages as lang


st.set_page_config(
    page_title="Free Speech-to-Text Transcription App | Faster-Whisper with Streamlit",
    page_icon="🎙️",
    layout="wide"
)


# -----------------------------
# Local Css All Buttons
# -----------------------------
def local_css(file_name: str):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
# Apply global styles
local_css("styles/style.css")

# -------------------------------
# Extract audio from video
# -------------------------------
def extract_audio_from_video(video_path):
    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
            audio_path = temp_audio.name

        clip = VideoFileClip(video_path)
        audio_clip = clip.audio

        if audio_clip is None:
            clip.close()
            return None
        logger = sl.StreamlitLogger()
        audio_clip.write_audiofile(audio_path, codec="pcm_s16le",logger=logger)
        audio_clip.close()
        clip.close()

        return audio_path
    except Exception as e:
        st.error(f"Error extracting audio: {e}")
        return None

# -------------------------------
# Transcribe with faster-whisper + progress bar
# -------------------------------
def transcribe_audio_with_timestamps(audio_path, model_size="base", language=None):
    try:
        model = WhisperModel(model_size, device="cpu", compute_type="int8")
        try:
            clip = AudioFileClip(audio_path)
            duration = clip.duration  # in seconds
            clip.close()
        except Exception:
            duration = None  # fallback if moviepy can't read duration

        segments, info = model.transcribe(audio_path, word_timestamps=True, language=language)

        results = {"language": info.language, "segments": []}

        # Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()

        for segment in segments:
            seg_data = {
                "start": segment.start,
                "end": segment.end,
                "text": segment.text.strip(),
                "words": []
            }

            if segment.words:
                for w in segment.words:
                    seg_data["words"].append({
                        "start": w.start,
                        "end": w.end,
                        "text": w.word.strip()
                    })

            results["segments"].append(seg_data)

            # ✅ Update progress
            if duration and duration > 0:
                progress = min(int((segment.end / duration) * 100), 100)
                progress_bar.progress(progress)
                status_text.text(f"⏳ Processing... {progress}%")
        
        # Complete
        progress_bar.progress(100)
        status_text.text("✅ Transcription complete!")

        return results

    except Exception as e:
        st.error(f"Error during transcription: {e}")
        return None

# -------------------------------
# Format transcription for CSV
# -------------------------------
def format_transcription_for_csv(transcription_results, include_words=False, chunk_size=None):
    formatted_data = []
    if transcription_results and "segments" in transcription_results:
        for segment in transcription_results["segments"]:
            words = segment.get("words", [])

            # case 1: chunking mode
            if chunk_size and words:
                for i in range(0, len(words), chunk_size):
                    chunk = words[i:i + chunk_size]
                    chunk_text = " ".join([w["text"] for w in chunk])
                    start_time = chunk[0]["start"]
                    end_time = chunk[-1]["end"]
                    formatted_data.append({
                        "start_time": start_time,
                        "end_time": end_time,
                        "text": chunk_text
                    })

            # case 2: include_words=True → add each word
            elif include_words and words:
                for w in words:
                    formatted_data.append({
                        "start_time": w["start"],
                        "end_time": w["end"],
                        "text": w["text"]
                    })

            # fallback: segment only
            else:
                formatted_data.append({
                    "start_time": segment["start"],
                    "end_time": segment["end"],
                    "text": segment["text"].strip()
                })
    return formatted_data


# -------------------------------
# Streamlit UI
# -------------------------------
def main():
    st.title("Free Speech-to-Text Transcription")
    st.write("Convert audio and video files into accurate text with our free Speech-to-Text Transcription App. Powered by Faster-Whisper and Streamlit, it supports multiple languages, timestamps, chunking, and CSV export. Fast, lightweight, and easy to use.")
    st.divider()

    
    CONFIG_PATH = "./.streamlit/config.toml"

    # Two theme presets
    THEMES = {
        "Light": {
            "theme": {
                "base": "light"
            },
        },
                "Dark": {
            "theme": {
                "base": "dark",
                "borderColor": "mediumSlateBlue"
            }
        }
    }  
    
    # Session state init
    if "df" not in st.session_state:
        st.session_state.df = None
    if "tmp_path" not in st.session_state:
        st.session_state.tmp_path = None
    if "audio_path" not in st.session_state:
        st.session_state.audio_path = None

    uploaded_file = st.file_uploader("Upload Audio/Video File", type=[
        "mp4", "avi", "mkv", "mov", "wmv", "flv",
        "wav", "mp3", "aac", "ogg", "flac"
    ])
    model_size = st.selectbox("Model size", ["tiny", "base", "small", "medium", "large"], index=1)
    # Language selection (default = English)

    selected_lang = st.selectbox("Select Language", list(lang.lang_map.keys()))
    language = lang.lang_map[selected_lang]


    # ✅ Always show this (was wrongly inside the else block before)
    include_words = st.checkbox("Include word-level timestamps", value=False)

    # New: chunk size input
    chunk_size = st.number_input(
        "Chunk size (number of words per row, set 0 to disable)",
        min_value=0, max_value=50, value=8, step=1
    )
    chunk_size = None if chunk_size == 0 else chunk_size

    # Process upload
    if uploaded_file is not None and st.session_state.tmp_path is None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
            tmp.write(uploaded_file.read())
            st.session_state.tmp_path = tmp.name

        st.success(f"File uploaded: {uploaded_file.name}")

    # -------------------------------
    # Buttons row
    # -------------------------------
    if "start_transcription" not in st.session_state:
        st.session_state.start_transcription = False

    # -------------------------------
    # Buttons row
    # -------------------------------
    # Create a layout that works better for buttons
    _, col2, col3 = st.columns([8, 4, 4])
    with col2:
        if st.button("Start Transcription", use_container_width=True):
            st.session_state.start_transcription = True
    with col3:
        if st.button("Clear All", use_container_width=True):
            st.session_state.start_transcription = False
            if st.session_state.audio_path and os.path.exists(st.session_state.audio_path):
                os.remove(st.session_state.audio_path)
            if st.session_state.tmp_path and os.path.exists(st.session_state.tmp_path):
                os.remove(st.session_state.tmp_path)
            st.session_state.df = None
            st.session_state.tmp_path = None
            st.session_state.audio_path = None
            st.rerun()

    # -------------------------------
    # Start transcription
    # -------------------------------
    if st.session_state.start_transcription and st.session_state.tmp_path:
        with st.spinner("⏳ Preparing transcription..."):
            ext = os.path.splitext(st.session_state.tmp_path)[1].lower()
            video_exts = [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv"]

            if ext in video_exts:
                st.session_state.audio_path = extract_audio_from_video(st.session_state.tmp_path)
            else:
                st.session_state.audio_path = st.session_state.tmp_path

        if not st.session_state.audio_path:
            st.error("No audio available for transcription.")
        else:
            with st.spinner("⏳ Transcription in progress..."):
                results = transcribe_audio_with_timestamps(
                    st.session_state.audio_path,
                    model_size=model_size,
                    language=language
                )

            if results:
                formatted = format_transcription_for_csv(
                    results,
                    include_words=include_words,
                    chunk_size=chunk_size
                )
                if formatted:
                    st.session_state.df = pd.DataFrame(formatted)
                else:
                    st.warning("No transcription data found.")

        st.session_state.start_transcription = False  # reset flag

    # -------------------------------
    # Show DataFrame if available
    # -------------------------------
    if st.session_state.df is not None:
        st.dataframe(st.session_state.df)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"transcription_{timestamp}.csv"

        csv = st.session_state.df.to_csv(index=False, encoding="utf-8-sig")
        st.download_button(
            "Download ⬇",
            data=csv,
            file_name=filename,
            mime="text/csv"
        )

    # Footer
    st.write("---")
    # Copyright (centered)
    year = datetime.datetime.now().year
    _, col, _ = st.columns([4, 2.5, 4])  # empty, center, empty
    with col:
        st.caption(f"© {year} All rights reserved.")

if __name__ == "__main__":
    main()
