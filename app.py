from dotenv import load_dotenv
import io
import base64
load_dotenv()

import streamlit as st
import os
from PIL import Image
import fitz  # Import PyMuPDF (as fitz)
import google.generativeai as genai

# Configure Google Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get response from Gemini
def get_gemini_response(input_text, pdf_content, prompt):    
    # model = genai.GenerativeModel("gemini-1.5-pro")
    model = genai.GenerativeModel("gemini-1.5-flash")
    # OR you can try:
    # model = genai.GenerativeModel("gemini-1.5-flash-latest") 
    # The 'latest' alias is often recommended for stability as it points to the most current stable version.    # pdf_content[0] is already in the format expected by Gemini
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text

# Function to convert PDF to image parts for Gemini using PyMuPDF
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        try:
            # Open the PDF from the uploaded bytes using PyMuPDF
            pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            
            # We only need the first page for Gemini's vision capability in this context
            first_page = pdf_document.load_page(0) 
            
            # Render the page to a pixmap (image)
            pix = first_page.get_pixmap()
            
            # Convert pixmap to a PIL Image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            # Convert PIL Image to bytes in JPEG format
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG')
            img_byte_arr = img_byte_arr.getvalue()

            # Prepare the image data in the format expected by Google Gemini API
            pdf_parts = [
                {
                    "mime_type": "image/jpeg",
                    "data": base64.b64encode(img_byte_arr).decode() # Encode to base64
                }
            ]
            return pdf_parts
        except Exception as e:
            st.error(f"Error processing PDF with PyMuPDF: {e}")
            return None
    else:
        raise FileNotFoundError("No file uploaded")
    
## Streamlit App Layout
st.set_page_config(page_title="ATS - Application Tracking System", page_icon=":guardsman:", layout="wide")
st.header("ATS - Application Tracking System")

input_text = st.text_area("Job Description", placeholder="Enter the job description here...", key="input")
uploaded_file = st.file_uploader("Upload your Resume (PDF)....", type=["pdf"], key="file_uploader")

if uploaded_file is not None:
    st.write("File uploaded successfully!")

# Buttons for different functionalities
submit1 = st.button("Tell me if I am a good fit for this job")
submit2 = st.button("Tell me About the Resume")
submit3 = st.button("How can I improve my skills")
submit4 = st.button("What are the key skills required for this job description?")
submit5 = st.button("Percentage Match")

# Prompts for Gemini
input_prompt1 = """
You are an experienced Technical Human Resource Manager with tech experience in field of any one job role Data Science, Web Development, Software Development, Big Data Analytics, DevOps, Data Analytics, 
Your task is to review the provided resume against the job description. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of any one job role Data Science, Web Development, Software Development, Big Data Analytics, DevOps, Data Analytics,  and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

# Logic for button clicks
if submit1:
    if uploaded_file is not None and input_text:
        pdf_content = input_pdf_setup(uploaded_file)
        if pdf_content: # Ensure PDF was processed successfully
            response = get_gemini_response(input_text, pdf_content, input_prompt3)
            st.subheader("The Response is")
            st.write(response)
    else:
        st.warning("Please upload a PDF file and enter the job description before submitting.")

if submit2:
    if uploaded_file is not None and input_text:
        pdf_content = input_pdf_setup(uploaded_file)
        if pdf_content: # Ensure PDF was processed successfully
            response = get_gemini_response(input_text, pdf_content, input_prompt1)
            st.subheader("The Response is")
            st.write(response)
    else:
        st.warning("Please upload a PDF file and enter the job description before submitting.")

if submit3:
    if uploaded_file is not None and input_text:
        pdf_content = input_pdf_setup(uploaded_file)
        if pdf_content: 
            response = get_gemini_response(input_text, pdf_content, input_prompt3) 
            st.subheader("The Response is")
            st.write(response)
    else:
        st.warning("Please upload a PDF file and enter the job description before submitting.")

if submit4:
    if uploaded_file is not None and input_text:
        pdf_content = input_pdf_setup(uploaded_file)
        if pdf_content: 
            response = get_gemini_response(input_text, pdf_content, input_prompt1) 
            st.subheader("The Response is")
            st.write(response)
    else:
        st.warning("Please upload a PDF file and enter the job description before submitting.")

if submit5:
    if uploaded_file is not None and input_text:
        pdf_content = input_pdf_setup(uploaded_file)
        if pdf_content: # Ensure PDF was processed successfully
            response = get_gemini_response(input_text, pdf_content, input_prompt3)
            st.subheader("The Response is")
            st.write(response)
    else:
        st.warning("Please upload a PDF file and enter the job description before submitting.")