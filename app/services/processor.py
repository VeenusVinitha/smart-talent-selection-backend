import fitz  # PyMuPDF
from docx import Document
from openai import OpenAI
import json
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("OPENROUTER_API_KEY")

)

def extract_text_from_file(file_path: str, extension: str):
    text = ""
    if extension == ".pdf":
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text()
    elif extension == ".docx":
        doc = Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    return text

def get_structured_profile(resume_text: str):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", # Switch to a more stable model
            response_format={ "type": "json_object" },
            messages=[
                {
                    "role": "system", 
                    "content": "You are a technical recruiter. Extract the following into JSON: "
                               "1. 'skills': A list of technical keywords. "
                               "2. 'years_of_experience': The total number of professional years as an integer. "
                               "Format: {'skills': [], 'years_of_experience': 0}"
                },
                {"role": "user", "content": resume_text}
            ]
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Extraction Error: {e}")
        return {"skills": [], "years_of_experience": 0}