import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ranker.py
# ranker.py
# ranker.py

def calculate_match(candidate_json, job_json):
    # --- 1. Skill Match (70% Weight) ---
    cand_skills = [s.lower().strip() for s in candidate_json.get("skills", [])]
    req_skills = [s.lower().strip() for s in job_json.get("skills", [])]
    
    skill_score = 0
    if req_skills:
        matches = 0
        for req in req_skills:
            # Flexible matching (e.g., 'React' matches 'React.js')
            if any(req in cand or cand in req for cand in cand_skills):
                matches += 1
        skill_score = (matches / len(req_skills)) * 100
    else:
        skill_score = 100

    # --- 2. Depth of Experience (30% Weight) ---
    cand_exp = float(candidate_json.get("years_of_experience", 0))
    req_exp = float(job_json.get("years_of_experience", 0))

    if req_exp > 0:
        # Penalize if they have less, reward up to 100 if they meet/exceed
        exp_score = min((cand_exp / req_exp) * 100, 100)
    else:
        # If JD doesn't specify exp, 1 year = 20 points, 5 years = 100 points
        exp_score = min(cand_exp * 20, 100) 

    # Weighted Calculation
    return round((skill_score * 0.7) + (exp_score * 0.3), 2)

# Ensure this function also uses gpt-4o-mini to avoid 429 errors
def generate_ai_summary(candidate_profile, job_description):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[
                {"role": "system", "content": "You are an HR expert. Write a 2-sentence 'Summary of Fit' for this candidate based on the JD. Be specific about skills and experience."},
                {"role": "user", "content": f"JD: {job_description}\nCandidate Profile: {candidate_profile}"}
            ]
        )
        return response.choices[0].message.content
    except Exception:
        return "Qualification match found based on technical skills and experience depth."