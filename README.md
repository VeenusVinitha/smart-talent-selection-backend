# Smart Talent Selection Dashboard

### The Problem
Recruiters struggle with manual screening and rigid keyword matching. Standard searches often miss the nuance of "years of experience" versus "skill mentions," leading to inefficient shortlisting of qualified candidates.

### The Solution
A full-stack AI-driven ranking dashboard. It utilizes a **70/30 weighted algorithm** (Skills vs. Experience) to rank candidates logically. By structuring resumes into JSON data via LLMs, it provides match scores and AI-generated "Summaries of Fit."

### Project Structure
* **/backend**: FastAPI server, PostgreSQL database logic, and AI ranking engine.
* **/frontend**: React.js dashboard built with TypeScript and Tailwind CSS.

### Tech Stack
* **Frontend:** React.js, TypeScript, Tailwind CSS, Axios, Lucide React.
* **Backend:** Python, FastAPI, SQLAlchemy (ORM), PostgreSQL.
* **AI Engine:** stepfun/step-3.5-flash:free via OpenRouter API.
* **Libraries:** PyMuPDF, pypdf, python-docx, python-dotenv.

---
### Setup Instructions(For my local system)

#### 1. Backend Setup
1. Open your terminal in the `/backend` folder.
2. Create a virtual environment: `python -m venv venv`
3. Activate it: 
   - Windows: `venv\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create a .env file with: OPENROUTER_API_KEY= key_from'.env'file

Run the server: uvicorn app.main:app --reload

#### 2. Frontend Setup
1. Open a new terminal in the /frontend folder.

2. Install dependencies: npm install

3. Start the application: npm run start

The dashboard will be available at http://localhost:3000.
