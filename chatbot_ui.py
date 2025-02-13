import streamlit as st
import requests
import time

st.title("LangChain Chatbot")

st.subheader("Upload Knowledge Base (PDF/TXT)")
uploaded_file = st.file_uploader("Upload a file", type=["pdf", "txt"])

if uploaded_file:
    with open(f"temp_{uploaded_file.name}", "wb") as f:
        f.write(uploaded_file.getbuffer())

    files = {"file": open(f"temp_{uploaded_file.name}", "rb")}
    response = requests.post("http://127.0.0.1:8000/upload/", files=files)

    if response.status_code == 200:
        st.success("File uploaded and processed successfully!")
    else:
        st.error("Error processing file!")

    time.sleep(2)

st.subheader("Chat with Your Knowledge Base")
user_input = st.text_input("Ask me anything:")

if st.button("Send"):
    response = requests.post("http://127.0.0.1:8000/ask/", json={"text": user_input}).json()
    st.write(response["response"])
