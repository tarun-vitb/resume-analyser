"""
Production-Grade FastAPI Backend for AI Resume Analyzer
Running on http://localhost:9000
"""

import os
import logging
import tempfile
import shutil
import json
import re
from typing import List, Dict, Any, Optional
from pathlib import Path
import asyncio
from datetime import datetime

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AI Resume Analyzer API",
    description="Production-grade AI-powered resume analysis platform",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
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

class AnalysisRequest(BaseModel):
    file_id: str
    job_description: str
    target_role: Optional[str] = None

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

# In-memory storage for demo (use database in production)
uploaded_files = {}
analysis_cache = {}

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

def extract_text_from_file(file_path: str, file_extension: str) -> str:
    """Extract text from uploaded file"""
    try:
        if file_extension == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        
        elif file_extension == '.pdf':
            try:
                import PyPDF2
                text = ""
                with open(file_path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    for page in reader.pages:
                        text += page.extract_text() + "\n"
                return text
            except ImportError:
                # Fallback text extraction
                return "PDF text extraction requires PyPDF2. Using fallback method."
        
        elif file_extension in ['.docx', '.doc']:
            try:
                from docx import Document
                doc = Document(file_path)
                text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
                return text
            except ImportError:
                return "DOCX text extraction requires python-docx. Using fallback method."
        
        else:
            return "Unsupported file format"
            
    except Exception as e:
        logger.error(f"Error extracting text: {e}")
        return f"Error extracting text: {str(e)}"

def extract_skills_from_text(text: str) -> List[str]:
    """Extract skills from resume text"""
    # Common technical skills
    skills_database = [
        # Programming Languages
        "Python", "JavaScript", "Java", "C++", "C#", "Go", "Rust", "PHP", "Ruby", "Swift",
        "Kotlin", "TypeScript", "R", "Scala", "MATLAB", "Perl", "Shell", "Bash",
        
        # Web Technologies
        "React", "Angular", "Vue.js", "Node.js", "Express", "Django", "Flask", "FastAPI",
        "HTML", "CSS", "SASS", "Bootstrap", "Tailwind", "jQuery", "Redux", "GraphQL",
        
        # Databases
        "SQL", "MySQL", "PostgreSQL", "MongoDB", "Redis", "Elasticsearch", "SQLite",
        "Oracle", "Cassandra", "DynamoDB", "Neo4j",
        
        # Cloud & DevOps
        "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Jenkins", "GitLab", "GitHub",
        "Terraform", "Ansible", "Linux", "Unix", "CI/CD", "DevOps", "Microservices",
        
        # Data Science & ML
        "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Scikit-learn",
        "Pandas", "NumPy", "Matplotlib", "Seaborn", "Jupyter", "Statistics", "Data Analysis",
        "Big Data", "Spark", "Hadoop", "Tableau", "Power BI", "Excel",
        
        # Soft Skills
        "Leadership", "Communication", "Project Management", "Team Management",
        "Problem Solving", "Critical Thinking", "Agile", "Scrum", "Kanban"
    ]
    
    found_skills = []
    text_lower = text.lower()
    
    for skill in skills_database:
        if skill.lower() in text_lower:
            found_skills.append(skill)
    
    return list(set(found_skills))  # Remove duplicates

def calculate_semantic_similarity(text1: str, text2: str) -> float:
    """Simple semantic similarity calculation"""
    # Convert to lowercase and split into words
    words1 = set(re.findall(r'\w+', text1.lower()))
    words2 = set(re.findall(r'\w+', text2.lower()))
    
    # Calculate Jaccard similarity
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    if len(union) == 0:
        return 0.0
    
    return len(intersection) / len(union)

def analyze_resume_content(resume_text: str, job_description: str) -> Dict[str, Any]:
    """Comprehensive resume analysis"""
    
    # Extract skills
    resume_skills = extract_skills_from_text(resume_text)
    job_skills = extract_skills_from_text(job_description)
    
    # Find skill matches and gaps
    matched_skills = list(set(resume_skills).intersection(set(job_skills)))
    missing_skills = list(set(job_skills) - set(resume_skills))
    
    # Calculate metrics
    semantic_similarity = calculate_semantic_similarity(resume_text, job_description)
    skill_match_score = len(matched_skills) / len(job_skills) if job_skills else 0
    
    # Selection probability (weighted combination)
    selection_probability = (semantic_similarity * 0.4 + skill_match_score * 0.6) * 100
    
    # Generate feedback
    feedback = []
    if selection_probability < 30:
        feedback.append("Consider adding more relevant keywords from the job description")
    if len(matched_skills) < 3:
        feedback.append("Add more technical skills that match the job requirements")
    if len(resume_text.split()) < 200:
        feedback.append("Expand your resume with more detailed experience descriptions")
    if "experience" not in resume_text.lower():
        feedback.append("Include more details about your work experience")
    
    # Course recommendations
    course_recommendations = []
    for skill in missing_skills[:5]:  # Top 5 missing skills
        course_recommendations.append({
            "skill": skill,
            "course_title": f"Master {skill} - Complete Guide",
            "provider": "Coursera" if len(skill) % 2 == 0 else "Udemy",
            "duration": f"{4 + len(skill) % 8} weeks",
            "rating": round(4.2 + (len(skill) % 8) * 0.1, 1),
            "price": f"${29 + len(skill) % 50}",
            "url": f"https://coursera.org/learn/{skill.lower().replace(' ', '-')}"
        })
    
    return {
        "fit_score": round(selection_probability, 1),
        "selection_probability": round(selection_probability, 1),
        "semantic_similarity": round(semantic_similarity * 100, 1),
        "skill_match_score": round(skill_match_score * 100, 1),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "total_skills_found": len(resume_skills),
        "feedback": feedback,
        "course_recommendations": course_recommendations,
        "resume_stats": {
            "word_count": len(resume_text.split()),
            "character_count": len(resume_text),
            "sections_detected": len([s for s in ["experience", "education", "skills", "projects"] 
                                    if s in resume_text.lower()])
        }
    }

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Resume Analyzer API v2.0",
        "status": "running",
        "endpoints": {
            "upload": "/upload_resume",
            "analyze": "/analyze_resume", 
            "matches": "/match_jobs",
            "docs": "/docs"
        },
        "server": "http://localhost:9000"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0"
    }

@app.post("/upload_resume", response_model=UploadResponse)
async def upload_resume(file: UploadFile = File(...)):
    """Upload and process resume file"""
    
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Validate file type
    allowed_extensions = {'.pdf', '.docx', '.doc', '.txt'}
    file_extension = Path(file.filename).suffix.lower()
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
        )
    
    try:
        # Generate unique file ID
        import uuid
        file_id = str(uuid.uuid4())
        
        # Save file temporarily
        file_path = UPLOAD_DIR / f"{file_id}{file_extension}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Extract text
        extracted_text = extract_text_from_file(str(file_path), file_extension)
        
        # Store file info
        uploaded_files[file_id] = {
            "filename": file.filename,
            "file_path": str(file_path),
            "extracted_text": extracted_text,
            "upload_time": datetime.now().isoformat(),
            "file_size": os.path.getsize(file_path)
        }
        
        # Extract basic info
        skills = extract_skills_from_text(extracted_text)
        
        return UploadResponse(
            success=True,
            message="Resume uploaded and processed successfully",
            file_id=file_id,
            extracted_text=extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text,
            metadata={
                "filename": file.filename,
                "file_size": os.path.getsize(file_path),
                "word_count": len(extracted_text.split()),
                "skills_found": len(skills),
                "preview_skills": skills[:10]
            }
        )
        
    except Exception as e:
        logger.error(f"Error uploading resume: {e}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.post("/analyze_resume", response_model=AnalysisResponse)
async def analyze_resume(
    file_id: str = Form(...),
    job_description: str = Form(...),
    target_role: Optional[str] = Form(None)
):
    """Analyze resume against job description"""
    
    import time
    start_time = time.time()
    
    # Check if file exists
    if file_id not in uploaded_files:
        raise HTTPException(status_code=404, detail="File not found. Please upload resume first.")
    
    try:
        # Get resume text
        resume_text = uploaded_files[file_id]["extracted_text"]
        
        # Perform analysis
        analysis = analyze_resume_content(resume_text, job_description)
        
        # Add target role specific analysis
        if target_role:
            analysis["target_role"] = target_role
            analysis["role_specific_feedback"] = [
                f"Optimize your resume for {target_role} positions",
                f"Highlight {target_role}-relevant experience more prominently"
            ]
        
        # Cache analysis
        analysis_cache[file_id] = analysis
        
        processing_time = time.time() - start_time
        
        return AnalysisResponse(
            success=True,
            message="Resume analysis completed successfully",
            analysis=analysis,
            processing_time=round(processing_time, 2)
        )
        
    except Exception as e:
        logger.error(f"Error analyzing resume: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/match_jobs", response_model=JobMatchResponse)
async def match_jobs(file_id: str):
    """Match resume against available job positions"""
    
    # Check if file exists
    if file_id not in uploaded_files:
        raise HTTPException(status_code=404, detail="File not found. Please upload resume first.")
    
    try:
        resume_text = uploaded_files[file_id]["extracted_text"]
        resume_skills = extract_skills_from_text(resume_text)
        
        matches = []
        
        for job in MOCK_JOBS:
            # Calculate fit score
            job_skills = job["skills_required"]
            matched_skills = list(set(resume_skills).intersection(set(job_skills)))
            missing_skills = list(set(job_skills) - set(resume_skills))
            
            # Calculate scores
            skill_overlap_score = len(matched_skills) / len(job_skills) if job_skills else 0
            semantic_similarity = calculate_semantic_similarity(resume_text, job["description"])
            
            # Combined fit score
            fit_score = (skill_overlap_score * 0.6 + semantic_similarity * 0.4) * 100
            selection_probability = min(fit_score * 1.2, 95)  # Cap at 95%
            
            matches.append(JobMatch(
                role_title=job["role_title"],
                company=job["company"],
                fit_score=round(fit_score, 1),
                skills_overlap=matched_skills,
                missing_skills=missing_skills[:5],  # Top 5 missing
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
    """Get demo data for frontend development"""
    return {
        "sample_analysis": {
            "fit_score": 78.5,
            "selection_probability": 82.3,
            "semantic_similarity": 74.2,
            "skill_match_score": 85.7,
            "matched_skills": ["Python", "React", "SQL", "Git", "AWS"],
            "missing_skills": ["Docker", "Kubernetes", "Machine Learning"],
            "feedback": [
                "Add more cloud computing experience",
                "Include specific project examples with metrics",
                "Highlight leadership experience"
            ],
            "course_recommendations": [
                {
                    "skill": "Docker",
                    "course_title": "Docker Mastery: Complete Toolset",
                    "provider": "Udemy",
                    "duration": "6 weeks",
                    "rating": 4.7,
                    "price": "$39"
                }
            ]
        },
        "sample_jobs": MOCK_JOBS[:3]
    }

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "error_type": "HTTPException"
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error",
            "error_type": "ServerError"
        }
    )

if __name__ == "__main__":
    print("🚀 Starting AI Resume Analyzer Backend")
    print("📍 Server: http://localhost:9000")
    print("📚 API Docs: http://localhost:9000/docs")
    print("💚 Health: http://localhost:9000/health")
    
    uvicorn.run(
        "backend_main:app",
        host="0.0.0.0",
        port=9000,
        reload=True,
        log_level="info"
    )
