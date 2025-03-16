import streamlit as st
from openai import OpenAI
import base64
import os
from google import genai
from google.genai import types
import fitz  # PyMuPDF


def main():
    st.title("Public Procurement Purchasing Law")
    st.write("Assistant for PPP - Law!")

    # File upload by user
    uploaded_file = st.file_uploader("Upload a Document (PDF)", type="pdf")
    if uploaded_file:
        question = st.text_input("Enter your question regarding the document:")

        if question:
            st.subheader("Generating Response...")
            
            # Choose method (Google GenAI or OpenAI)
            method = st.selectbox("Choose an API for processing:", ["Google GenAI", "OpenAI"])
            
            if method == "Google GenAI":
                result = generate_with_google_genai(uploaded_file)
                st.write("Google GenAI Response: ", result)
            
            elif method == "OpenAI":
                response_stream = generate_with_openai(uploaded_file, question)
                for chunk in response_stream:
                    st.write(chunk['choices'][0]['message']['content'])

if __name__ == "__main__":
    main()
