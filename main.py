import streamlit as st
from vtt_to_transcript import vtt_to_plain_text
import io

# Sidebar navigation
st.sidebar.markdown("## Table of Contents")
st.sidebar.markdown("[VTT to Plain Text](#vtt-to-plain-text)")
st.sidebar.markdown("[Video Transcription Checklist](#video-transcription-checklist)")
"""
VTT to Plain Text
=================
"""
st.markdown('<div id="vtt-to-plain-text"></div>', unsafe_allow_html=True)

st.markdown("""
            Please upload a VTT file to convert to a plain text file. The converted file will be available for download.
            """)

# Create file uploader
uploaded_file = st.file_uploader("Upload a VTT file", type="vtt")

# Convert the uploaded file to a plain text file
if uploaded_file is not None:
    converted_file_path = vtt_to_plain_text(io.BytesIO(uploaded_file.getvalue()), uploaded_file.name)
    
    if converted_file_path is not None:
        # Read the converted file content for download
        with open(converted_file_path, 'r') as f:
            converted_content = f.read()
        
        st.success(f"File converted successfully!")
        st.download_button(
            label="Download Converted File",
            data=converted_content,
            file_name=converted_file_path,
            mime="text/plain"
        )
    else:
        st.error("Error converting file. Please try again.")
else:
    st.info("Please upload a VTT file to convert to a plain text file.")

"""
Video Transcription Checklist
=============================
"""

# Initialize session state for these checklists
checklist_keys: list[str] = [
    "vimeo_processed",
    "first_frame_processed",
    "closed_captioning_processed",
    "transcript_processed",
    "vimeo_link_working",
    "video_download_available",
    "transcript_download_available"
]

st.markdown('<div id="video-transcription-checklist"></div>', unsafe_allow_html=True)
st.markdown("""
            Below is a rough checklist to make sure all videos are processed correctly for Canvas usage.
            """)

# Add reset button
if st.button("Reset Checklist"):
    for key in checklist_keys:
        st.session_state[key] = False
    st.rerun()

# Create the checklist
st.checkbox("Video is processed on Vimeo",
            key="vimeo_processed")
st.checkbox("Video's first frame is just the intro slide along with the webcam(s) of the presenter(s)",
            key="first_frame_processed")
st.checkbox("Video has closed captioning (from Rev)",
            key="closed_captioning_processed")
st.checkbox("Transcript has been formed with screenshots from the video and the closed captions",
            key="transcript_processed")
st.checkbox("player.vimeo.com/video/<video_id> is working correctly",
            key="vimeo_link_working")
st.checkbox("Video is available for download",
            key="video_download_available")
st.checkbox("Transcript is available for download",
            key="transcript_download_available")