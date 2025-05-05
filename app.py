import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from google_doc_helper import save_chat_to_google_doc

# Load .env variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize Gemini model
model = genai.GenerativeModel("gemini-1.5-pro")

# Set Streamlit layout
st.set_page_config(page_title="Gemini Chatbot", layout="centered")
st.title("💬 Gemini Chatbot")

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display all messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
prompt = st.chat_input("Type your message...")

if prompt:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Gemini response
        response = model.generate_content(prompt)
        reply = response.text

        # Add assistant message
        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.markdown(reply)

    except Exception as e:
        st.error(f"Error: {e}")

# Action buttons
st.markdown("### Actions")
col1, col2 = st.columns(2)

# Save chat to Google Docs
if col1.button("💾 Save Chat to Google Doc"):
    if st.session_state.messages:
        try:
            link = save_chat_to_google_doc(st.session_state.messages)
            st.success(f"Chat saved! [Open Document]({link})")
        except Exception as e:
            st.error(f"Failed to save: {e}")
    else:
        st.warning("No messages to save.")

# Clear chat
if col2.button("🧹 Clear Chat"):
    st.session_state.messages = []
    st.rerun()



