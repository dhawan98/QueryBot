from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import os
import shutil
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

app = FastAPI()
os.environ["OPENAI_API_KEY"] = "your-api-key-here"

UPLOAD_DIR = "uploads/"
VECTORSTORE_DIR = "vectorstore/"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(VECTORSTORE_DIR, exist_ok=True)

class Query(BaseModel):
    text: str

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

def process_files():
    docs = []
    for file_name in os.listdir(UPLOAD_DIR):
        file_path = os.path.join(UPLOAD_DIR, file_name)

        try:
            print(f"🔍 Processing file: {file_path}")

            if file_name.endswith(".pdf"):
                loader = PyPDFLoader(file_path)
            elif file_name.endswith(".txt"):
                loader = TextLoader(file_path, encoding="utf-8")
            else:
                print(f"⚠️ Skipping unsupported file: {file_name}")
                continue

            loaded_docs = loader.load()
            print(f"✅ Successfully loaded {file_name}")

            docs.extend(loaded_docs)

        except Exception as e:
            print(f"❌ Error loading {file_name}: {str(e)}")

    if not docs:
        print("❌ No valid documents found!")
        return

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(docs)

    vectorstore = FAISS.from_documents(texts, OpenAIEmbeddings())
    vectorstore.save_local(VECTORSTORE_DIR)

    print("✅ Knowledge base updated successfully!")

@app.post("/upload/")
async def upload_file(file: UploadFile):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print(f"✅ File uploaded successfully: {file_path}")

        # Check if file is readable
        with open(file_path, "r", encoding="utf-8") as f:
            print(f"🔍 File preview: {f.read(500)}")

        process_files()

        return {"message": f"{file.filename} uploaded and processed successfully!"}

    except Exception as e:
        print(f"❌ Error processing file: {str(e)}")
        return {"error": "Failed to process the file"}

def load_retriever():
    return FAISS.load_local(VECTORSTORE_DIR, OpenAIEmbeddings())

@app.post("/ask/")
async def ask(query: Query):
    retriever = load_retriever()
    llm = ChatOpenAI(model_name="gpt-3.5-turbo")
    qa_chain = ConversationalRetrievalChain.from_llm(llm, retriever.as_retriever(), memory=memory)

    response = qa_chain.run({"question": query.text, "chat_history": memory.load_memory_variables({})})
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
