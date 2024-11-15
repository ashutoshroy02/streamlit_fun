import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

# Load environment variables
load_dotenv()  

# Configure the API key for Google Generative AI
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
genai.configure(api_key = 'AIzaSyBYU6sCd9c6xSPDQIcfxCfd7VMJ2si3GSs')

# Define the function to generate Gemini response
def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

# Function to extract text from PDF
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Prompt Template for the Gemini model
input_prompt = """
Hey Act Like a skilled or very experienced ATS(Application Tracking System)
with a deep understanding of tech fields, software engineering, data science, data analysis,
and big data engineering. Your task is to evaluate the resume based on the given job description.
You must consider the job market as very competitive and provide the best assistance for improving the resumes.
Assign the percentage Matching based on JD and the missing keywords with high accuracy.
resume:{text}
description:{jd}

I want the response in one single string with the structure
{{"JD Match":"%","MissingKeywords":[],"Profile Summary":""}}
"""

# CSS for animated background
css = """
<style>
body {
  margin: 0;
  padding: 0;
  text-align: left;
  min-height: 100vh;
  background-image: linear-gradient(80deg, rgb(5, 124, 172), rgb(199, 10, 114));
  overflow: hidden;
}
#up, #down, #left, #right {
    position: absolute;
    border-radius: 50%;
    filter: blur(80px);
    animation: fadeIn 40s infinite;
}
#up {
    height: 800px; width: 800px; background-image: linear-gradient(80deg, rgb(5, 124, 172), rgba(43, 247, 202, 0.5));
    animation: down 40s infinite;
}
#down {
    right: 0; height: 500px; width: 500px; background-image: linear-gradient(80deg, rgba(245, 207, 82, 0.8), rgba(199, 10, 114));
    animation: up 30s infinite;
}
#left {
    height: 500px; width: 500px; background-image: linear-gradient(80deg, rgb(199, 10, 160), rgba(183, 253, 52, 0.8));
    animation: left 40s 1s infinite;
}
#right {
    height: 500px; width: 500px; background-image: linear-gradient(80deg, rgba(26, 248, 18, 0.6), rgba(199, 10, 52, 0.8));
    animation: right 30s .5s infinite;
}
@keyframes fadeIn { 0% { opacity: 0; } 100% { opacity: 1; } }
@keyframes down { 0%, 100% { top: -100px; } 70% { top: 700px; } }
@keyframes up { 0%, 100% { bottom: -100px; } 70% { bottom: 700px; } }
@keyframes left { 0%, 100% { left: -100px; } 70% { left: 1000px; } }
@keyframes right { 0%, 100% { right: -100px; } 70% { right: 1000px; } }
</style>
"""

# HTML for animated sections
html = """
<section id="up"></section>
<section id="down"></section>
<section id="left"></section>
<section id="right"></section>
"""

# Streamlit UI
st.markdown(css, unsafe_allow_html=True)
st.markdown(html, unsafe_allow_html=True)

st.title("Smart ATS")
st.text("Improve Your Resume ATS Compatibility")

# Input fields for job description and file upload
jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload a PDF file.")

# Submit button to process the data
submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        # Extract text from PDF and generate response
        text = input_pdf_text(uploaded_file)
        prompt = input_prompt.format(text=text, jd=jd)
        response = get_gemini_response(prompt)
        st.subheader("ATS Evaluation Results")
        st.text(response)
    else:
        st.warning("Please upload a resume file.")
