import google.generativeai as genai
import os
import PyPDF2 as pdf

# Configure the generative AI model
genai.configure(api_key="Your API Key")
model = genai.GenerativeModel("gemini-pro")


# Function to get response from the Generative AI model
def get_gemini_response(input_text):
    response = model.generate_content(input_text)
    return response.text  # Adjust based on the actual response structure


# Function to extract text from an uploaded PDF file
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page_number in range(len(reader.pages)):
        page = reader.pages[page_number]
        text += str(page.extract_text())
    return text


# Prompt template
input_prompt = """Hey, act like a skilled or very experienced ATS (Applicant Tracking System) with a deep understanding of the tech field, software engineering, data science, data analysis, and big data engineering. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide the best assistance for improving the resumes. Assign the percentage matching based on the job description and the missing keywords like missing TECHNOLOGY STACK, SKILL and QUALIFICATIONS based on job the description.
Resume: {resume_text}
Description: {jd_text}
I want the response in one single string having the structure {{ "JD Match": "%", "MissingKeywords": [], "Profile Summary": "" }}
"""


# Function to generate ATS evaluation
def evaluate_resume_against_jd(resume_text, jd_text):
    prompt = input_prompt.format(resume_text=resume_text, jd_text=jd_text)
    response = get_gemini_response(prompt)
    return response


# Example usage
if __name__ == "__main__":
    resume_file_path = input("Resume File Path")
    job_description = input("Job Description")
    print(resume_file_path, job_description)
    with open(resume_file_path, "rb") as uploaded_file:
        resume_text = input_pdf_text(uploaded_file)
    ats_evaluation = evaluate_resume_against_jd(resume_text, job_description)
    print(ats_evaluation)
