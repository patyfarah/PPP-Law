import streamlit as st
from openai import OpenAI
import base64
import os
from google import genai
from google.genai import types
import fitz  # PyMuPDF


import streamlit as st
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings.google import GoogleGenerativeAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import GoogleGenerativeAI
import os

# Set Gemini API Key (Replace with your own key or use environment variables)
# Access the API key from the environment variable
api_key = os.getenv("API_KEY")
os.environ['GOOGLE_API_KEY'] = api_key
# Load and Process PDFs
def load_and_chunk_pdfs(pdf_paths):
    docs = []
    for pdf_path in pdf_paths:
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = text_splitter.split_documents(documents)
        docs.extend(chunks)
    return docs

# Initialize FAISS Vector Store
def create_vector_store(docs):
    embeddings = GoogleGenerativeAIEmbeddings()
    vector_store = FAISS.from_documents(docs, embeddings)
    return vector_store

# Load PDFs (Preloaded Files)
pdf_files = ["example1.pdf", "example2.pdf"]  # Replace with actual file paths
docs = load_and_chunk_pdfs(pdf_files)
vector_store = create_vector_store(docs)
retriever = vector_store.as_retriever()
qa_chain = RetrievalQA.from_chain_type(llm=GoogleGenerativeAI(), retriever=retriever)

# Streamlit UI
st.title("PDF-based Q&A Chatbot")
st.write("Ask questions based on preloaded PDFs")

user_query = st.text_input("Enter your question:")
if user_query:
    response = qa_chain.run(user_query)
    st.write("### Response:")
    st.write(response)



