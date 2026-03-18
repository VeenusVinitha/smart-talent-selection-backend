from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.core.database import get_db, engine, Base
from app.services.parser import extract_text
import app.models.schemas as models
from pydantic import BaseModel
from app.services.ranker import calculate_match, generate_ai_summary
from app.services.processor import get_structured_profile, extract_text_from_file
import os
from typing import List
import uuid



app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#Define the structure of the incoming request
class JDRequest(BaseModel):
    jd_text: str
# Create database tables
Base.metadata.create_all(bind=engine)

@app.post("/upload")
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    # Parse the file and extract text
    file.file.seek(0)
    text = extract_text(file.file)
    
    new_candidate = models.Candidate(
        filename=file.filename,
        full_text=text
    )
    db.add(new_candidate)
    db.commit()
    db.refresh(new_candidate)

    return {"id": new_candidate.id, "status": "Saved to Database"}




from typing import List

@app.post("/parse-resume")
async def parse_resume(files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    results = []
    
    for file in files:
        # Generate a unique temp filename to avoid collisions during concurrent uploads
        unique_id = uuid.uuid4().hex
        extension = os.path.splitext(file.filename)[1].lower()
        temp_path = f"temp_{unique_id}_{file.filename}"
        
        try:
            # Save file locally
            with open(temp_path, "wb") as buffer:
                buffer.write(await file.read())

            # Process the file
            resume_text = extract_text_from_file(temp_path, extension)
            if not resume_text:
                continue 

            profile = get_structured_profile(resume_text)
            
            # Add to database
            new_candidate = models.Candidate(
                filename=file.filename,
                resume_text=resume_text,
                candidate_profile_json=profile
            )
            db.add(new_candidate)
            results.append({"filename": file.filename, "profile": profile})
            
        except Exception as e:
            print(f"Error processing {file.filename}: {e}")
            # Continue to next file even if one fails
            continue
            
        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    db.commit()
    return {"status": "Success", "processed_count": len(results), "profiles": results}

# Upload Job Description
@app.post("/upload-job")
async def upload_job(request: JDRequest, db: Session = Depends(get_db)):
    structured_jd = get_structured_profile(request.jd_text) 
    
    # Add a print here to see the results in your terminal
    print(f"AI extracted from JD: {structured_jd}")

    new_job = models.Job(
        job_description=request.jd_text,
        job_profile_json=structured_jd
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return {
        "message": "Job Description saved", 
        "job_id": new_job.job_id,
        "extracted_skills": structured_jd.get("skills") # Helpful for debugging
    }

#Candidate Ranking
@app.post("/rank-candidates/{job_id}")
async def rank_candidates(job_id: int, db: Session = Depends(get_db)):
    job = db.query(models.Job).filter(models.Job.job_id == job_id).first()
    candidates = db.query(models.Candidate).all()
    
    ranked_list = []
    for cand in candidates:
        score = calculate_match(cand.candidate_profile_json, job.job_profile_json)
        summary = generate_ai_summary(cand.candidate_profile_json, job.job_description)
        
        ranked_list.append({
            "candidate_id": cand.id,
            "name": cand.filename,
            "score": score,
            "summary": summary, 
            "skills": cand.candidate_profile_json.get("skills", [])
        })
    
    ranked_list.sort(key=lambda x: x["score"], reverse=True)
    return ranked_list

@app.get("/candidates")
async def get_all_candidates(db: Session = Depends(get_db)):
    candidates = db.query(models.Candidate).all()
    return candidates
