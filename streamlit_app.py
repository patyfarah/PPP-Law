import streamlit as st
from openai import OpenAI
import PyPDF2

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        str: The extracted text.
    """
    text = ""
    try:
        with open(pdf_path, 'rb') as file:  # 'rb' for read binary
            reader = PyPDF2.PdfReader(file)  # Updated for PyPDF2 3.0+

            for page_num in range(len(reader.pages)):  # Corrected attribute
                page = reader.pages[page_num]         # Access pages using index
                text += page.extract_text()
    except FileNotFoundError:
        return "Error: File not found."
    except Exception as e:
        return f"Error: An error occurred: {e}"

    return text

# Show title and description.
st.title("Public Procurement Purchasing Law")
st.write(
    "Assistant for PPP - Law!"
)

# Create an OpenAI client.
client = OpenAI(api_key="sk-...DyQA")

# Let the user upload a file via `st.file_uploader`.
uploaded_file = st.file_uploader(
"Upload a document (.pdf)", type=("pdf")
)

# Ask the user for a question via `st.text_area`.
question = st.text_area(
"Now ask a question about the document!",
placeholder="Can you give me a short summary?",
disabled=not uploaded_file,
)
if uploaded_file and question:

    # Process the uploaded file and question.
    document = uploaded_file.read().decode()
    messages = [
        {
            "role": "user",
            "content": f"Here's a document: {document} \n\n---\n\n {question}",
        }
    ]
    
    # Generate an answer using the OpenAI API.
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        stream=True,
    )
    
    # Stream the response to the app using `st.write_stream`.
    st.write_stream(stream)
