from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from app.core.database import Base
import datetime

class Candidate(Base):
    __tablename__ = "candidates"
    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String) 
    filename = Column(String)
    upload_date = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String, default="Uploaded") 
    resume_text = Column(Text) 
    candidate_profile_json = Column(JSONB)

class Job(Base):
    __tablename__ = "jobs"
    job_id = Column(Integer, primary_key=True, index=True)
    job_title = Column(String)
    job_description = Column(Text)
    job_profile_json = Column(JSONB) 
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
