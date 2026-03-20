import fitz  # PyMuPDF
from docx import Document
from openai import OpenAI
import json
import os
from dotenv import load_dotenv
import pytesseract
from PIL import Image

import pytesseract

# This tells Python where the actual engine is installed
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


#C:\Users\User\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

load_dotenv()

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("OPENROUTER_API_KEY")

)


def extract_text_from_file(file_path: str, extension: str):
    text = ""
    extension = extension.lower() # Ensure case-insensitivity

    if extension == ".pdf":
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text()
            
    elif extension == ".docx":
        doc = Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
            
    elif extension in [".jpg", ".jpeg", ".png"]:
        # Open the image using PIL
        img = Image.open(file_path)
        # Use pytesseract to extract text
        text = pytesseract.image_to_string(img)
        
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
