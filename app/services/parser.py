import pypdf
from fastapi import HTTPException

def extract_text(file_obj) -> str:
    """Requirement: Intelligent Parsing of non-linear layouts."""
    try:
        reader = pypdf.PdfReader(file_obj)
        full_text = ""
        for page in reader.pages:
            # extract_text() handles multi-column resumes better than basic tools 
            full_text += page.extract_text() + "\n"
        
        if not full_text.strip():
            raise ValueError("File appears empty or unreadable ")
        return full_text
    except Exception as e:
        print(f"Parsing error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Parsing error: {str(e)}")