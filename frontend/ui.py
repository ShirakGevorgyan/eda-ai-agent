import streamlit as st
import requests

# Set the page title and icon
st.set_page_config(page_title="Synopsys EDA AI Agent", page_icon="🤖")

st.title("🤖 EDA AI Agent")
st.markdown("### Ask questions about your Verilog, SDC, and Tcl files")

# 1. Setup the Backend URL (our FastAPI server)
API_URL = "http://127.0.0.1:8000/api/v1/chat/send"

# 2. Initialize Chat History
# This keeps the messages on the screen
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Display Chat Messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. User Input Area
if prompt := st.chat_input("What is the period of the clock?"):
    # Add user message to history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 5. Send request to our FastAPI Backend
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # We send the message to our API
                response = requests.post(API_URL, json={"message": prompt})
                
                if response.status_code == 200:
                    ai_answer = response.json().get("ai_response")
                    st.markdown(ai_answer)
                    # Add AI response to history
                    st.session_state.messages.append({"role": "assistant", "content": ai_answer})
                else:
                    st.error("Error: Could not reach the AI server.")
            except Exception as e:
                st.error(f"Connection error: {e}")