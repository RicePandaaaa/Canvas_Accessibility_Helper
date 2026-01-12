import streamlit as st
from vtt_to_transcript import vtt_to_plain_text
import io

# Sidebar navigation
st.sidebar.markdown("## Table of Contents")
st.sidebar.markdown("[VTT to Plain Text](#vtt-to-plain-text)")

# Main content with sections
st.markdown('<div id="vtt-to-plain-text"></div>', unsafe_allow_html=True)
st.header("VTT to Plain Text")

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