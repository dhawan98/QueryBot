# AI-Powered Chatbot with User-Uploaded Knowledge Base

## 📌 Project Description  
This project is an **AI-powered chatbot** built using **LangChain, OpenAI, FastAPI, and Streamlit**. Unlike standard chatbots, this system allows users to **upload their own PDFs and TXT files**, which the AI then processes and uses for answering questions.  

By leveraging **Retrieval-Augmented Generation (RAG)**, the chatbot retrieves relevant information from uploaded documents and generates responses using **GPT-3.5**. The system also maintains **chat memory**, enabling contextual conversations.  

### 🔹 Use Cases  
✅ Technical Documentation Assistance  
✅ Company Knowledge Base  
✅ Research Paper Summaries  
✅ Legal or Medical FAQ Chatbots  

---

## 📜 Features  
✔️ **Upload Your Own Knowledge Base** (Supports PDF & TXT)  
✔️ **Retrieval-Augmented Generation (RAG)** for Accurate Answers  
✔️ **Conversational Memory** (Remembers previous queries)  
✔️ **FastAPI Backend for Scalability**  
✔️ **Streamlit UI for Easy Interaction**  
✔️ **Uses FAISS for Fast Vector Search**  

---

## 🛠️ Tech Stack  
- **Python**  
- **LangChain** (For RAG & Memory)  
- **OpenAI API** (GPT-3.5 for response generation)  
- **FAISS** (Vector Database for Efficient Search)  
- **FastAPI** (Backend API)  
- **Streamlit** (Frontend UI)  
- **PyPDF & TextLoader** (Document Processing)  

---

## 📌 Running the Project  

### 1️⃣ Start the Backend (FastAPI)  
Run the following command:  
python chatbot_api.py    
This will run FastAPI on http://127.0.0.1:8000.
### 2️⃣ Start the Frontend (Streamlit)    
Run the following command:   
streamlit run chatbot_ui.py   
This will open the chatbot UI in your browser.




