import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import streamlit as st
import requests
from app.core.config import settings


st.set_page_config(page_title="Synopsys EDA Agent", page_icon="🤖", layout="wide")
st.title("🤖 EDA AI Agent")

CHAT_URL = "http://127.0.0.1:8000/api/v1/chat/send"
UPLOAD_URL = "http://127.0.0.1:8000/api/v1/documents/upload"

with st.sidebar:
    st.header("⚙️ Settings")
    
    selected_model = st.selectbox(
        "Choose AI Model:",
        options=settings.AVAILABLE_MODELS
    )
    
    st.divider()
    
    st.header("📁 Upload Documents")
    uploaded_file = st.file_uploader("Choose a Verilog, SDC, or PDF file", type=["v", "sv", "sdc", "pdf", "txt", "tcl"])
    
    if st.button("Upload and Index"):
        if uploaded_file is not None:
            with st.spinner("Uploading and processing..."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
                response = requests.post(UPLOAD_URL, files=files)
                
                if response.status_code == 200:
                    st.success(f"Success! {uploaded_file.name} is now in AI memory.")
                else:
                    st.error("Failed to upload file.")
        else:
            st.warning("Please select a file first.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about your hardware design..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Inside user input block
    with st.chat_message("assistant"):
        with st.spinner("Analyzing files with Local AI (this can take 1-2 minutes on CPU)..."):
            try:
                payload = {"message": prompt, "model_name": selected_model}
                # Added timeout=300 (5 minutes)
                response = requests.post(CHAT_URL, json=payload, timeout=300)
                
                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("ai_response")
                    st.markdown(answer)
                else:
                    st.error(f"Backend Error: {response.status_code} - {response.text}")
            except requests.exceptions.Timeout:
                st.error("The AI is taking too long to answer. Please check your CPU load.")
            except Exception as e:
                st.error(f"Connection error: {e}")