import streamlit as st
import google.generativeai as genai
import os
import numpy

# Set up the page
st.set_page_config(page_title="My AI Chatbot", page_icon="🤖")
st.title("🤖 My AI Chatbot")
st.write("Gemini 2.5 Flash")
st.progress(0.999)


api_key = None


try:
    api_key = st.secrets["GEMINI_API_KEY"]
    st.sidebar.success("✅ API Key loaded from secrets")
except:
    pass
st.sidebar.write("Aathif Faizal")

if not api_key:
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        st.sidebar.success("✅ API Key loaded from environment")

if not api_key:
    with st.sidebar:
        st.header("Setup")
        api_key = st.text_input("Enter your Gemini API Key:", type="password")
        if api_key:
            st.success("API Key entered!")
        else:
            st.warning("Please add your API key to start chatting")

if api_key:
    genai.configure(api_key=api_key)


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What would you like to know?"):
    if not api_key:
        st.error("Please add your API key first!")
        st.stop()
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Create the model
                model = genai.GenerativeModel('gemini-2.0-flash-exp')
                
                # Generate response
                response = model.generate_content(prompt)
                
                # Show response
                st.markdown(response.text)
                
                # Add AI response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Clear chat button
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()