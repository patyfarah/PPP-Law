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
            method = st.selectbox("Choose an API for processing:", ["Google GenAI"])
            
            if method == "Google GenAI":
                result = generate_with_google_genai(uploaded_file)
                st.write("Google GenAI Response: ", result)
            
            elif method == "OpenAI":
                response_stream = generate_with_openai(uploaded_file, question)
                for chunk in response_stream:
                    st.write(chunk['choices'][0]['message']['content'])

if __name__ == "__main__":
    main()
def generate_with_google_genai(uploaded_file):
    client = genai.Client(
        api_key=os.environ.get("AIzaSyCuRhWVr4-SJ8APQyIvcKDtmA_Cww3pH9M"),
    )

    files = [uploaded_file]
   model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_uri(
                    file_uri=files[0].uri,
                    mime_type=files[0].mime_type,
                ),
                types.Part.from_text(text="""INSERT_INPUT_HERE"""),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text="""answer from uploaded document"""),
        ],
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")


