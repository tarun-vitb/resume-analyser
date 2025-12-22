"""
Simple AI Resume Analyzer Backend - No Complex Dependencies
Fixed for Windows and local development
"""

import os
import logging
import tempfile
import shutil
import json
import re
from typing import List, Dict, Any, Optional
from pathlib import Path
import uuid
from datetime import datetime

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AI Resume Analyzer API",
    description="Simple AI-powered resume analysis",
    version="2.0.0"
)

# CORS Configuration for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create directories
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Pydantic Models
class UploadResponse(BaseModel):
    success: bool
    message: str
    file_id: str
    extracted_text: str
    metadata: Dict[str, Any]

class AnalysisResponse(BaseModel):
    success: bool
    message: str
    analysis: Dict[str, Any]
    processing_time: float

class JobMatch(BaseModel):
    role_title: str
    company: str
    fit_score: float
    skills_overlap: List[str]
    missing_skills: List[str]
    selection_probability: float
    salary_range: Optional[str] = None

class JobMatchResponse(BaseModel):
    success: bool
    matches: List[JobMatch]
    total_matches: int

# In-memory storage
uploaded_files = {}

# Mock job database
MOCK_JOBS = [
    {
        "role_title": "Senior Software Engineer",
        "company": "TechCorp Inc.",
        "description": "Looking for a senior software engineer with expertise in Python, React, AWS, and machine learning. 5+ years experience required.",
        "skills_required": ["Python", "React", "AWS", "Machine Learning", "Docker", "SQL"],
        "salary_range": "$120k - $160k"
    },
    {
        "role_title": "Data Scientist",
        "company": "DataFlow Analytics", 
        "description": "Seeking a data scientist with strong Python, SQL, and machine learning skills. Experience with TensorFlow and cloud platforms preferred.",
        "skills_required": ["Python", "SQL", "Machine Learning", "TensorFlow", "Statistics", "Pandas"],
        "salary_range": "$110k - $150k"
    },
    {
        "role_title": "Full Stack Developer",
        "company": "StartupXYZ",
        "description": "Full stack developer needed with React, Node.js, and database experience. Fast-paced startup environment.",
        "skills_required": ["React", "Node.js", "JavaScript", "MongoDB", "Git", "CSS"],
        "salary_range": "$90k - $130k"
    },
    {
        "role_title": "DevOps Engineer", 
        "company": "CloudTech Solutions",
        "description": "DevOps engineer with AWS, Docker, Kubernetes experience. CI/CD pipeline management required.",
        "skills_required": ["AWS", "Docker", "Kubernetes", "Jenkins", "Linux", "Python"],
        "salary_range": "$100k - $140k"
    },
    {
        "role_title": "Machine Learning Engineer",
        "company": "AI Innovations",
        "description": "ML engineer to build and deploy machine learning models. Python, TensorFlow, and cloud experience essential.",
        "skills_required": ["Python", "TensorFlow", "Machine Learning", "AWS", "Docker", "MLOps"],
        "salary_range": "$130k - $170k"
    }
]

def extract_text_simple(file_path: str, file_extension: str) -> str:
    """Simple text extraction without complex dependencies"""
    try:
        if file_extension == '.txt':
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        
        elif file_extension == '.pdf':
            # Simple PDF text extraction fallback
            try:
                import PyPDF2
                text = ""
                with open(file_path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    for page in reader.pages:
                        text += page.extract_text() + "\n"
                return text
            except ImportError:
                # Fallback for PDF without PyPDF2
                return "PDF processing not available. Please install PyPDF2 or use TXT files for testing."
        
        elif file_extension in ['.docx', '.doc']:
            try:
                from docx import Document
                doc = Document(file_path)
                text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
                return text
            except ImportError:
                return "DOCX processing not available. Please install python-docx or use TXT files for testing."
        
        else:
            return "Unsupported file format. Please use PDF, DOCX, or TXT files."
            
    except Exception as e:
        logger.error(f"Error extracting text: {e}")
        return f"Error extracting text: {str(e)}"

def extract_skills_simple(text: str) -> List[str]:
    """Simple skill extraction using keyword matching"""
    skills_database = [
        # Programming Languages
        "Python", "JavaScript", "Java", "C++", "C#", "Go", "Rust", "PHP", "Ruby", "Swift",
        "Kotlin", "TypeScript", "R", "Scala", "MATLAB", "HTML", "CSS",
        
        # Web Technologies
        "React", "Angular", "Vue.js", "Node.js", "Express", "Django", "Flask", "FastAPI",
        "Bootstrap", "Tailwind", "jQuery", "Redux", "GraphQL", "REST", "API",
        
        # Databases
        "SQL", "MySQL", "PostgreSQL", "MongoDB", "Redis", "Elasticsearch", "SQLite",
        "Oracle", "Cassandra", "DynamoDB",
        
        # Cloud & DevOps
        "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Jenkins", "GitLab", "GitHub",
        "Terraform", "Ansible", "Linux", "Unix", "CI/CD", "DevOps",
        
    ]
    
    text_lower = text.lower()
    found = [skill.title() for skill in skills if skill in text_lower]
    return list(set(found))

def calculate_fit_score(resume_text: str, job_desc: str, resume_skills: List[str]) -> tuple:
    # Semantic similarity
    embeddings = model.encode([resume_text, job_desc])
    similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    
    # Skill matching
    job_skills = extract_skills(job_desc)
    resume_skills_lower = [s.lower() for s in resume_skills]
    job_skills_lower = [s.lower() for s in job_skills]
    
    matching = sum(1 for skill in job_skills_lower if skill in resume_skills_lower)
    skill_ratio = matching / max(len(job_skills), 1) if job_skills else 0.5
    
    # Combined score
    fit_score = int((similarity * 0.6 + skill_ratio * 0.4) * 100)
    fit_score = max(25, min(95, fit_score))
    
    # Shortlist probability
    shortlist = int(fit_score * 0.8 + np.random.randint(-8, 12))
    shortlist = max(15, min(88, shortlist))
    
    # Missing skills
    missing = [skill for skill in job_skills if skill.lower() not in resume_skills_lower]
    
    return fit_score, shortlist, missing[:6]

def get_courses(missing_skills: List[str]) -> List[Dict[str, str]]:
    courses = {
        'python': {'name': 'Python Programming', 'link': 'https://www.coursera.org/learn/python'},
        'javascript': {'name': 'JavaScript Essentials', 'link': 'https://www.udemy.com/course/javascript-essentials/'},
        'react': {'name': 'React Complete Guide', 'link': 'https://www.udemy.com/course/react-the-complete-guide/'},
        'machine learning': {'name': 'ML Specialization', 'link': 'https://www.coursera.org/specializations/machine-learning-introduction'},
        'aws': {'name': 'AWS Cloud Practitioner', 'link': 'https://www.udemy.com/course/aws-certified-cloud-practitioner/'},
        'docker': {'name': 'Docker Mastery', 'link': 'https://www.udemy.com/course/docker-mastery/'},
        'sql': {'name': 'SQL for Data Science', 'link': 'https://www.coursera.org/learn/sql-for-data-science'}
    }
    
    result = []
    for skill in missing_skills[:4]:
        skill_lower = skill.lower()
        if skill_lower in courses:
            result.append(courses[skill_lower])
        else:
            result.append({
                'name': f'Learn {skill}',
                'link': f'https://www.coursera.org/search?query={skill.replace(" ", "+")}'
            })
    
    return result

def get_feedback(fit_score: int) -> str:
    if fit_score < 50:
        return "Focus on adding relevant skills and experience that match the job requirements. Highlight your achievements with specific examples."
    elif fit_score < 75:
        return "Good foundation! Add more relevant keywords and quantify your achievements with numbers and results."
    else:
        return "Excellent match! Fine-tune by adding specific project examples and measurable outcomes to stand out."

def get_job_matches(skills: List[str]) -> List[Dict[str, Any]]:
    jobs = {
        'Software Developer': ['python', 'javascript', 'react', 'sql', 'git'],
        'Data Scientist': ['python', 'machine learning', 'pandas', 'sql', 'tensorflow'],
        'DevOps Engineer': ['docker', 'kubernetes', 'aws', 'linux', 'jenkins'],
        'Frontend Developer': ['javascript', 'react', 'html', 'css', 'typescript'],
        'Backend Developer': ['python', 'sql', 'rest api', 'node.js', 'mongodb'],
        'Full Stack Developer': ['javascript', 'react', 'node.js', 'sql', 'html']
    }
    
    matches = []
    skills_lower = [s.lower() for s in skills]
    
    for job, required in jobs.items():
        score = sum(1 for req in required if req in skills_lower)
        if score > 0:
            fit = min(92, 50 + (score * 8))
            matches.append({'title': job, 'fit_score': fit})
    
    return sorted(matches, key=lambda x: x['fit_score'], reverse=True)[:4]

@app.post("/upload_resume")
async def upload_resume(file: UploadFile = File(...)):
    global resume_data
    
    if not file.filename.lower().endswith(('.pdf', '.docx')):
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files supported")
    
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        if file.filename.lower().endswith('.pdf'):
            text = extract_pdf_text(tmp_path)
        else:
            text = extract_docx_text(tmp_path)
        
        os.unlink(tmp_path)
        
        if not text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from file")
        
        name = extract_name(text)
        skills = extract_skills(text)
        
        resume_data = {'name': name, 'skills': skills, 'text': text}
        
        return {
            'message': 'Resume uploaded successfully',
            'name': name,
            'skills': skills
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

@app.post("/analyze")
async def analyze(request: AnalysisRequest):
    if not resume_data:
        raise HTTPException(status_code=400, detail="Please upload a resume first")
    
    if not request.job_description.strip():
        raise HTTPException(status_code=400, detail="Job description is required")
    
    try:
        name = resume_data['name']
        skills = resume_data['skills']
        text = resume_data['text']
        
        fit_score, shortlist_prob, missing_skills = calculate_fit_score(
            text, request.job_description, skills
        
        for job in MOCK_JOBS:
            job_skills = job["skills_required"]
            matched_skills = list(set(resume_skills).intersection(set(job_skills)))
            missing_skills = list(set(job_skills) - set(resume_skills))
            
            # Calculate scores
            skill_overlap_score = len(matched_skills) / len(job_skills) if job_skills else 0
            semantic_similarity = calculate_similarity_simple(resume_text, job["description"])
            
            fit_score = (skill_overlap_score * 0.6 + semantic_similarity * 0.4) * 100
            selection_probability = min(fit_score * 1.2, 95)
            
            matches.append(JobMatch(
                role_title=job["role_title"],
                company=job["company"],
                fit_score=round(fit_score, 1),
                skills_overlap=matched_skills,
                missing_skills=missing_skills[:5],
                selection_probability=round(selection_probability, 1),
                salary_range=job.get("salary_range")
            ))
        
        # Sort by fit score
        matches.sort(key=lambda x: x.fit_score, reverse=True)
        
        return JobMatchResponse(
            success=True,
            matches=matches,
            total_matches=len(matches)
        )
        
    except Exception as e:
        logger.error(f"Error matching jobs: {e}")
        raise HTTPException(status_code=500, detail=f"Job matching failed: {str(e)}")

@app.get("/demo_data")
async def get_demo_data():
    """Demo data for testing"""
    return {
        "sample_analysis": {
            "fit_score": 78.5,
            "selection_probability": 82.3,
            "matched_skills": ["Python", "React", "SQL", "Git", "AWS"],
            "missing_skills": ["Docker", "Kubernetes", "Machine Learning"],
            "feedback": [
                "Add more cloud computing experience",
                "Include specific project metrics",
                "Highlight leadership experience"
            ]
        },
        "sample_jobs": MOCK_JOBS[:3]
    }

if __name__ == "__main__":
    print("🚀 Starting Simple AI Resume Analyzer Backend")
    print("📍 Server: http://localhost:9000")
    print("📚 API Docs: http://localhost:9000/docs")
    print("💚 Health: http://localhost:9000/health")
    print("🎨 Frontend: http://localhost:5173")
    
    uvicorn.run(
        "simple_backend:app",
        host="0.0.0.0",
        port=9000,
        reload=True,
        log_level="info"
    )
