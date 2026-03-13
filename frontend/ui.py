import streamlit as st
import requests

st.set_page_config(page_title="Synopsys EDA Agent", page_icon="🤖", layout="wide")
st.title("🤖 EDA AI Agent")

CHAT_URL = "http://127.0.0.1:8000/api/v1/chat/send"
UPLOAD_URL = "http://127.0.0.1:8000/api/v1/documents/upload"

with st.sidebar:
    st.header("⚙️ Settings")
    
    selected_model = st.selectbox(
        "Choose AI Model:",
        ["gpt-4o", "gpt-3.5-turbo", "llama3 (local)"]
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

    with st.chat_message("assistant"):
        with st.spinner("Analyzing files..."):
            payload = {
                "message": prompt,
                "model_name": selected_model
            }
            response = requests.post(CHAT_URL, json=payload)
            
            
            if response.status_code == 200:
                data = response.json()
                answer = data.get("ai_response")
                performance = data.get("performance") # Get time from backend
                
                st.markdown(answer)
                st.caption(f"⏱️ Response time: {performance}") # Show time below answer
                
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                st.error("Error communicating with Backend.")