import sys
import os
import requests
import streamlit as st

# 1. Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.core.config import settings

# 2. Page Configuration
st.set_page_config(page_title="Synopsys EDA Agent", page_icon="🤖", layout="wide")

# 3. Sidebar for Settings and Uploads
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Model Selection
    selected_model = st.selectbox(
        "Choose AI Model:",
        options=settings.AVAILABLE_MODELS,
        help="OpenAI is fast. Llama is local and private."
    )
    
    # Clear Chat Button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    
    st.header("📁 Upload Documents")
    uploaded_file = st.file_uploader(
        "Upload Verilog, SDC, or Tcl files", 
        type=["v", "sv", "sdc", "pdf", "txt", "tcl"]
    )
    
    if st.button("🚀 Upload and Index"):
        if uploaded_file:
            with st.spinner("Processing file..."):
                UPLOAD_URL = f"{os.getenv('BACKEND_URL', 'http://127.0.0.1:8000')}/api/v1/documents/upload"
                files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
                try:
                    response = requests.post(UPLOAD_URL, files=files)
                    if response.status_code == 200:
                        st.success(f"Successfully indexed: {uploaded_file.name}")
                    else:
                        st.error("Upload failed.")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please select a file.")

# 4. Main Chat Interface
st.title("🤖 Synopsys EDA AI Agent")
st.info("Agentic AI for Hardware Design & Timing Analysis")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "model" in message:
            st.caption(f"Model: {message['model']} | ⏱️ {message.get('time', 'N/A')}")

# User Input
if prompt := st.chat_input("Ask about your hardware design (e.g., Explain the clock constraints)..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant Response
    with st.chat_message("assistant"):
        # DYNAMIC SPINNER TEXT based on the selected model
        spinner_text = "Thinking..."
        if "llama" in selected_model.lower():
            spinner_text = "Running Local AI (Llama 3.1) on CPU. This may take a minute..."
        
        with st.spinner(spinner_text):
            try:
                CHAT_URL = f"{os.getenv('BACKEND_URL', 'http://127.0.0.1:8000')}/api/v1/chat/send"
                payload = {"message": prompt, "model_name": selected_model}
                
                response = requests.post(CHAT_URL, json=payload, timeout=300)
                
                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("ai_response")
                    perf = data.get("performance", "N/A")
                    
                    st.markdown(answer)
                    st.caption(f"Model: {selected_model} | ⏱️ Response time: {perf}")
                    
                    # Store response in session state
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": answer, 
                        "model": selected_model, 
                        "time": perf
                    })
                else:
                    st.error(f"Backend Error {response.status_code}")
            except Exception as e:
                st.error(f"Error: {e}")