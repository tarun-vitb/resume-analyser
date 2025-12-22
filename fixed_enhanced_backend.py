"""
Fixed Enhanced AI Resume Analyzer Backend
Ensures proper skill matching and only shows eligible job vacancies
"""

import os
import logging
import tempfile
import shutil
import json
import re
from typing import List, Dict, Any, Optional, Set, Tuple
from pathlib import Path
import uuid
from datetime import datetime
import math

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Fixed Enhanced AI Resume Analyzer API",
    description="Advanced AI-powered resume analysis with accurate skill matching",
    version="3.1.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create directories
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Global storage
uploaded_files = {}

# Enhanced Skills Database with Categories
COMPREHENSIVE_SKILLS_DB = {
    "Programming Languages": [
        "Python", "JavaScript", "Java", "C++", "C#", "TypeScript", "Go", "Rust", 
        "PHP", "Ruby", "Swift", "Kotlin", "Scala", "R", "MATLAB", "Perl", "Dart",
        "C", "Objective-C", "Shell Scripting", "PowerShell", "VBA", "Assembly"
    ],
    "Web Technologies": [
        "React", "Angular", "Vue.js", "HTML", "CSS", "Sass", "Less", "Bootstrap",
        "Tailwind CSS", "jQuery", "Node.js", "Express.js", "Next.js", "Nuxt.js",
        "Svelte", "Ember.js", "Backbone.js", "D3.js", "Three.js", "WebGL"
    ],
    "Backend & APIs": [
        "REST APIs", "GraphQL", "FastAPI", "Django", "Flask", "Spring Boot",
        "ASP.NET", "Laravel", "Ruby on Rails", "Express.js", "Koa.js", "Nest.js",
        "Microservices", "API Gateway", "WebSockets", "gRPC", "SOAP", "OpenAPI"
    ],
    "Databases": [
        "SQL", "MySQL", "PostgreSQL", "MongoDB", "Redis", "Cassandra", "DynamoDB",
        "Oracle", "SQL Server", "SQLite", "Neo4j", "InfluxDB", "CouchDB",
        "MariaDB", "Firebase", "Supabase", "PlanetScale", "Elasticsearch"
    ],
    "Cloud & DevOps": [
        "AWS", "Azure", "Google Cloud", "Docker", "Kubernetes", "Jenkins", "GitLab CI",
        "GitHub Actions", "Terraform", "Ansible", "Chef", "Puppet", "Vagrant",
        "CloudFormation", "Serverless", "Lambda", "Azure Functions", "Cloud Functions"
    ],
    "Data Science & ML": [
        "Machine Learning", "Deep Learning", "Data Analysis", "Pandas", "NumPy",
        "Scikit-learn", "TensorFlow", "PyTorch", "Keras", "OpenCV", "NLTK", "spaCy",
        "Matplotlib", "Seaborn", "Plotly", "Jupyter", "Apache Spark", "Hadoop",
        "Statistics", "Data Mining", "Computer Vision", "NLP", "MLOps", "Databricks"
    ],
    "Mobile Development": [
        "React Native", "Flutter", "iOS Development", "Android Development", "Xamarin",
        "Ionic", "Cordova", "Swift", "Kotlin", "Objective-C", "Java", "Dart"
    ],
    "Tools & Frameworks": [
        "Git", "SVN", "Mercurial", "Jira", "Confluence", "Slack", "Teams", "Zoom",
        "Figma", "Adobe XD", "Sketch", "InVision", "Zeplin", "Postman", "Insomnia",
        "VS Code", "IntelliJ", "Eclipse", "Vim", "Emacs"
    ],
    "Testing & QA": [
        "Jest", "Mocha", "Chai", "Cypress", "Selenium", "Playwright", "Puppeteer",
        "JUnit", "TestNG", "PyTest", "RSpec", "Cucumber", "Postman", "SoapUI",
        "Load Testing", "Performance Testing", "Unit Testing", "Integration Testing"
    ],
    "Security": [
        "Cybersecurity", "Penetration Testing", "OWASP", "SSL/TLS", "OAuth", "JWT",
        "SAML", "Active Directory", "LDAP", "Firewall", "VPN", "Encryption",
        "Security Auditing", "Vulnerability Assessment", "SIEM", "SOC"
    ]
}

# Real Company Data with Job Openings
REAL_COMPANY_JOBS = [
    {
        "company": "Google",
        "role_title": "Senior Software Engineer",
        "required_skills": ["Python", "Java", "Machine Learning", "TensorFlow", "Google Cloud", "Kubernetes"],
        "preferred_skills": ["Go", "C++", "Deep Learning", "Docker"],
        "salary_range": "$180k - $250k",
        "location": "Mountain View, CA",
        "experience_level": "Senior",
        "job_type": "Full-time",
        "minimum_match_threshold": 50  # Minimum % of required skills needed
    },
    {
        "company": "Microsoft",
        "role_title": "Cloud Solutions Architect",
        "required_skills": ["Azure", "C#", "PowerShell", "Microservices", "Docker", "Kubernetes"],
        "preferred_skills": ["Python", "Terraform", "Azure Functions", "DevOps"],
        "salary_range": "$160k - $220k",
        "location": "Seattle, WA",
        "experience_level": "Senior",
        "job_type": "Full-time",
        "minimum_match_threshold": 40
    },
    {
        "company": "Amazon",
        "role_title": "Data Scientist",
        "required_skills": ["Python", "Machine Learning", "AWS", "SQL", "Statistics", "Pandas"],
        "preferred_skills": ["R", "Spark", "Deep Learning", "TensorFlow", "PyTorch"],
        "salary_range": "$150k - $200k",
        "location": "Seattle, WA",
        "experience_level": "Mid-Senior",
        "job_type": "Full-time",
        "minimum_match_threshold": 45
    },
    {
        "company": "Meta",
        "role_title": "Frontend Engineer",
        "required_skills": ["React", "JavaScript", "TypeScript", "HTML", "CSS", "GraphQL"],
        "preferred_skills": ["React Native", "Node.js", "Jest", "Webpack"],
        "salary_range": "$170k - $230k",
        "location": "Menlo Park, CA",
        "experience_level": "Mid-Senior",
        "job_type": "Full-time",
        "minimum_match_threshold": 50
    },
    {
        "company": "Netflix",
        "role_title": "Machine Learning Engineer",
        "required_skills": ["Python", "Machine Learning", "TensorFlow", "PyTorch", "AWS", "Spark"],
        "preferred_skills": ["Scala", "Java", "Kubernetes", "MLOps", "Deep Learning"],
        "salary_range": "$190k - $280k",
        "location": "Los Gatos, CA",
        "experience_level": "Senior",
        "job_type": "Full-time",
        "minimum_match_threshold": 55
    },
    {
        "company": "Apple",
        "role_title": "iOS Developer",
        "required_skills": ["Swift", "iOS Development", "Objective-C", "Xcode"],
        "preferred_skills": ["SwiftUI", "Combine", "Core ML", "ARKit"],
        "salary_range": "$160k - $220k",
        "location": "Cupertino, CA",
        "experience_level": "Mid-Senior",
        "job_type": "Full-time",
        "minimum_match_threshold": 60
    },
    {
        "company": "Tesla",
        "role_title": "Full Stack Developer",
        "required_skills": ["React", "Node.js", "Python", "PostgreSQL", "Docker"],
        "preferred_skills": ["TypeScript", "GraphQL", "Redis", "Kubernetes", "AWS"],
        "salary_range": "$140k - $190k",
        "location": "Austin, TX",
        "experience_level": "Mid-Senior",
        "job_type": "Full-time",
        "minimum_match_threshold": 40
    },
    {
        "company": "Spotify",
        "role_title": "Backend Engineer",
        "required_skills": ["Java", "Python", "Microservices", "PostgreSQL", "Docker"],
        "preferred_skills": ["Scala", "Kubernetes", "Google Cloud", "GraphQL", "Kafka"],
        "salary_range": "$150k - $200k",
        "location": "New York, NY",
        "experience_level": "Mid-Senior",
        "job_type": "Full-time",
        "minimum_match_threshold": 45
    }
]

# Pydantic Models
class UploadResponse(BaseModel):
    success: bool
    message: str
    file_id: str
    extracted_text: str
    metadata: Dict[str, Any]
    extracted_skills: List[str]
    skill_categories: Dict[str, List[str]]

class AnalysisResponse(BaseModel):
    success: bool
    message: str
    analysis: Dict[str, Any]
    processing_time: float

class JobMatch(BaseModel):
    company: str
    role_title: str
    fit_score: float
    skills_overlap: List[str]
    missing_skills: List[str]
    selection_probability: float
    salary_range: str
    location: str
    experience_level: str
    skill_match_percentage: float
    exact_matches: int
    total_required: int
    eligibility_reason: str

class JobMatchResponse(BaseModel):
    success: bool
    matches: List[JobMatch]
    total_matches: int
    eligible_matches: int
    best_fit_company: str
    average_fit_score: float

def extract_text_simple(file_path: str, file_extension: str) -> str:
    """Enhanced text extraction with better formatting"""
    try:
        if file_extension == '.txt':
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                return file.read()
        elif file_extension == '.pdf':
            try:
                import fitz  # PyMuPDF
                doc = fitz.open(file_path)
                text = ""
                for page in doc:
                    text += page.get_text()
                doc.close()
                return text
            except ImportError:
                return "PDF processing requires PyMuPDF. Install with: pip install PyMuPDF"
        elif file_extension in ['.docx', '.doc']:
            try:
                from docx import Document
                doc = Document(file_path)
                text = ""
                for paragraph in doc.paragraphs:
                    text += paragraph.text + "\n"
                return text
            except ImportError:
                return "DOCX processing requires python-docx. Install with: pip install python-docx"
        else:
            return "Unsupported file format"
    except Exception as e:
        return f"Error extracting text: {str(e)}"

def extract_skills_enhanced(text: str) -> Tuple[Dict[str, List[str]], List[str]]:
    """Enhanced skill extraction with exact matching and categorization"""
    if not text or not text.strip():
        return {}, []
    
    text_lower = text.lower()
    
    # Clean and normalize text - be more permissive with special characters
    text_normalized = re.sub(r'[^\w\s+#.-]', ' ', text_lower)
    text_normalized = re.sub(r'\s+', ' ', text_normalized).strip()
    
    categorized_skills = {}
    all_found_skills = []
    
    for category, skills_list in COMPREHENSIVE_SKILLS_DB.items():
        found_skills = []
        
        for skill in skills_list:
            skill_lower = skill.lower()
            
            # Multiple pattern matching strategies
            patterns = []
            
            # For single letter skills like "R"
            if len(skill_lower) == 1:
                patterns = [
                    rf'\b{re.escape(skill_lower)}\b',  # Word boundary
                    rf'(?:^|\s){re.escape(skill_lower)}(?:\s|$|,|\.|;)',  # Start/end with punctuation
                    rf'{re.escape(skill_lower)}\s+programming',  # "R programming"
                    rf'{re.escape(skill_lower)}\s+language',  # "R language"
                ]
            else:
                # For multi-word skills
                patterns = [
                    rf'\b{re.escape(skill_lower)}\b',  # Exact word match
                    rf'(?:^|\s){re.escape(skill_lower)}(?:\s|$|,|\.|;)',  # Word boundary with punctuation
                ]
                
                # Special handling for compound skills with special characters
                if any(char in skill_lower for char in ['.', '+', '#', '-']):
                    patterns.append(re.escape(skill_lower))
                
                # Handle variations like "machine learning" vs "ml"
                if skill_lower == "machine learning":
                    patterns.extend([r'\bml\b', r'\bmachine\s+learning\b'])
                elif skill_lower == "artificial intelligence":
                    patterns.extend([r'\bai\b', r'\bartificial\s+intelligence\b'])
            
            # Check all patterns
            skill_found = False
            for pattern in patterns:
                try:
                    if re.search(pattern, text_normalized):
                        if skill not in found_skills:
                            found_skills.append(skill)
                            all_found_skills.append(skill)
                            skill_found = True
                        break
                except re.error:
                    # Skip invalid regex patterns
                    continue
            
            if skill_found:
                continue
        
        if found_skills:
            categorized_skills[category] = found_skills
    
    return categorized_skills, all_found_skills

def calculate_exact_match_percentage(resume_skills: List[str], job_skills: List[str]) -> Dict[str, Any]:
    """Calculate exact skill match percentages with case-insensitive matching"""
    if not job_skills:
        return {
            "matched_skills": [],
            "missing_skills": [],
            "extra_skills": resume_skills,
            "match_percentage": 0.0,
            "matched_count": 0,
            "total_required": 0,
            "extra_count": len(resume_skills)
        }
    
    resume_skills_lower = [skill.lower().strip() for skill in resume_skills]
    job_skills_lower = [skill.lower().strip() for skill in job_skills]
    
    matched_skills = []
    missing_skills = []
    
    # Find matches
    for job_skill in job_skills:
        job_skill_lower = job_skill.lower().strip()
        if job_skill_lower in resume_skills_lower:
            matched_skills.append(job_skill)
        else:
            missing_skills.append(job_skill)
    
    # Find extra skills (in resume but not in job requirements)
    extra_skills = []
    for resume_skill in resume_skills:
        resume_skill_lower = resume_skill.lower().strip()
        if resume_skill_lower not in job_skills_lower:
            extra_skills.append(resume_skill)
    
    total_job_skills = len(job_skills)
    matched_count = len(matched_skills)
    
    match_percentage = (matched_count / total_job_skills * 100) if total_job_skills > 0 else 0
    
    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "extra_skills": extra_skills,
        "match_percentage": round(match_percentage, 1),
        "matched_count": matched_count,
        "total_required": total_job_skills,
        "extra_count": len(extra_skills)
    }

def analyze_resume_comprehensive(resume_text: str, job_description: str) -> Dict[str, Any]:
    """Comprehensive resume analysis with exact percentages"""
    
    # Extract skills with categories
    resume_skill_categories, resume_skills = extract_skills_enhanced(resume_text)
    job_skill_categories, job_skills = extract_skills_enhanced(job_description)
    
    # Debug logging
    logger.info(f"Resume skills found: {len(resume_skills)} - {resume_skills[:10]}")
    logger.info(f"Job skills found: {len(job_skills)} - {job_skills[:10]}")
    
    # Calculate exact matches
    match_analysis = calculate_exact_match_percentage(resume_skills, job_skills)
    
    # Category-wise analysis
    category_analysis = {}
    for category in COMPREHENSIVE_SKILLS_DB.keys():
        resume_cat_skills = resume_skill_categories.get(category, [])
        job_cat_skills = job_skill_categories.get(category, [])
        
        if job_cat_skills:  # Only analyze categories that are required
            cat_analysis = calculate_exact_match_percentage(resume_cat_skills, job_cat_skills)
            category_analysis[category] = {
                "required": job_cat_skills,
                "matched": cat_analysis["matched_skills"],
                "missing": cat_analysis["missing_skills"],
                "match_percentage": cat_analysis["match_percentage"]
            }
    
    # Calculate overall scores
    skill_match_score = match_analysis["match_percentage"]
    
    # Selection probability based on skill match and other factors
    base_probability = skill_match_score
    
    # Boost for having extra relevant skills
    extra_skill_boost = min(len(match_analysis["extra_skills"]) * 2, 15)
    
    # Experience factor (simple heuristic based on text length and keywords)
    experience_keywords = ["years", "experience", "worked", "developed", "managed", "led", "created"]
    experience_mentions = sum(1 for keyword in experience_keywords if keyword in resume_text.lower())
    experience_factor = min(experience_mentions * 3, 20)
    
    selection_probability = min(base_probability + extra_skill_boost + experience_factor, 95)
    
    # Fit score (weighted combination)
    fit_score = (skill_match_score * 0.6 + selection_probability * 0.4)
    
    # Generate feedback
    feedback = []
    if skill_match_score >= 80:
        feedback.append("Excellent skill match! You're well-qualified for this position.")
    elif skill_match_score >= 60:
        feedback.append("Good skill foundation with room for improvement.")
    elif skill_match_score >= 30:
        feedback.append("Some relevant skills found. Consider developing more aligned skills.")
    else:
        feedback.append("Limited skill match. Focus on developing relevant skills for this role.")
    
    if match_analysis["missing_skills"]:
        critical_missing = match_analysis["missing_skills"][:3]  # Top 3 missing
        feedback.append(f"Focus on developing: {', '.join(critical_missing)}")
    
    if match_analysis["extra_skills"]:
        feedback.append(f"Great! You have {len(match_analysis['extra_skills'])} bonus skills that add value.")
    
    # Course recommendations for missing skills
    course_recommendations = []
    for skill in match_analysis["missing_skills"][:5]:  # Top 5 missing skills
        course_recommendations.append({
            "skill": skill,
            "course_title": f"Master {skill} - Complete Guide",
            "provider": "Professional Training",
            "duration": "6-8 weeks",
            "rating": 4.7,
            "price": "$49-99",
            "priority": "High" if skill in match_analysis["missing_skills"][:2] else "Medium"
        })
    
    return {
        "fit_score": round(fit_score, 1),
        "selection_probability": round(selection_probability, 1),
        "skill_match_score": round(skill_match_score, 1),
        "matched_skills": match_analysis["matched_skills"],
        "missing_skills": match_analysis["missing_skills"],
        "extra_skills": match_analysis["extra_skills"],
        "total_skills_found": len(resume_skills),
        "total_job_skills": len(job_skills),
        "exact_matches": match_analysis["matched_count"],
        "skill_analysis": category_analysis,
        "feedback": feedback,
        "course_recommendations": course_recommendations,
        "resume_stats": {
            "word_count": len(resume_text.split()),
            "character_count": len(resume_text.strip()),
            "skill_categories_found": len(resume_skill_categories),
            "total_unique_skills": len(resume_skills)
        }
    }

def match_jobs_realtime(resume_skills: List[str]) -> List[JobMatch]:
    """Real-time job matching with eligibility filtering"""
    matches = []
    
    logger.info(f"Matching against resume skills: {resume_skills}")
    
    for job in REAL_COMPANY_JOBS:
        required_skills = job["required_skills"]
        preferred_skills = job.get("preferred_skills", [])
        all_job_skills = required_skills + preferred_skills
        
        # Calculate match for required skills only (for eligibility)
        required_match_analysis = calculate_exact_match_percentage(resume_skills, required_skills)
        required_match_percentage = required_match_analysis["match_percentage"]
        
        # Calculate match for all skills (for overall fit score)
        all_match_analysis = calculate_exact_match_percentage(resume_skills, all_job_skills)
        
        # Check eligibility based on minimum threshold
        minimum_threshold = job.get("minimum_match_threshold", 30)
        is_eligible = required_match_percentage >= minimum_threshold
        
        if not is_eligible:
            # Skip this job if not eligible
            continue
        
        # Calculate weighted fit score (required skills are more important)
        required_matches = len(required_match_analysis["matched_skills"])
        preferred_matches = len([skill for skill in preferred_skills if skill in resume_skills])
        
        required_weight = 0.7
        preferred_weight = 0.3
        
        required_score = (required_matches / len(required_skills) * 100) if required_skills else 0
        preferred_score = (preferred_matches / len(preferred_skills) * 100) if preferred_skills else 0
        
        fit_score = (required_score * required_weight) + (preferred_score * preferred_weight)
        
        # Selection probability
        selection_probability = min(fit_score + (len(all_match_analysis["extra_skills"]) * 1.5), 95)
        
        # Eligibility reason
        eligibility_reason = f"Meets {required_match_percentage:.1f}% of required skills (minimum: {minimum_threshold}%)"
        
        matches.append(JobMatch(
            company=job["company"],
            role_title=job["role_title"],
            fit_score=round(fit_score, 1),
            skills_overlap=all_match_analysis["matched_skills"],
            missing_skills=all_match_analysis["missing_skills"],
            selection_probability=round(selection_probability, 1),
            salary_range=job["salary_range"],
            location=job["location"],
            experience_level=job["experience_level"],
            skill_match_percentage=round(all_match_analysis["match_percentage"], 1),
            exact_matches=all_match_analysis["matched_count"],
            total_required=len(all_job_skills),
            eligibility_reason=eligibility_reason
        ))
    
    # Sort by fit score
    matches.sort(key=lambda x: x.fit_score, reverse=True)
    
    logger.info(f"Found {len(matches)} eligible job matches")
    
    return matches

# API Endpoints
@app.get("/api")
async def root():
    """API root endpoint"""
    return {"message": "Fixed Enhanced AI Resume Analyzer API", "version": "3.1.0"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/upload_resume", response_model=UploadResponse)
async def upload_resume(file: UploadFile = File(...)):
    """Upload and process resume file with enhanced skill extraction"""
    
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    allowed_extensions = {'.pdf', '.docx', '.doc', '.txt'}
    file_extension = Path(file.filename).suffix.lower()
    
    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    
    try:
        file_id = str(uuid.uuid4())
        file_path = UPLOAD_DIR / f"{file_id}{file_extension}"
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        extracted_text = extract_text_simple(str(file_path), file_extension)
        skill_categories, all_skills = extract_skills_enhanced(extracted_text)
        
        logger.info(f"Uploaded file {file.filename}: {len(all_skills)} skills found")
        
        uploaded_files[file_id] = {
            "filename": file.filename,
            "file_path": str(file_path),
            "extracted_text": extracted_text,
            "upload_time": datetime.now().isoformat(),
            "file_size": os.path.getsize(file_path),
            "skills": all_skills,
            "skill_categories": skill_categories
        }
        
        return UploadResponse(
            success=True,
            message="Resume uploaded and processed successfully",
            file_id=file_id,
            extracted_text=extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text,
            metadata={
                "filename": file.filename,
                "file_size": os.path.getsize(file_path),
                "word_count": len(extracted_text.split()),
                "total_skills_found": len(all_skills),
                "skill_categories_count": len(skill_categories)
            },
            extracted_skills=all_skills,
            skill_categories=skill_categories
        )
        
    except Exception as e:
        logger.error(f"Error uploading resume: {e}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.post("/analyze_resume", response_model=AnalysisResponse)
async def analyze_resume(file_id: str = Form(...), job_description: str = Form(...)):
    """Analyze resume with comprehensive skill matching"""
    
    if file_id not in uploaded_files:
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        start_time = datetime.now()
        
        resume_text = uploaded_files[file_id]["extracted_text"]
        analysis = analyze_resume_comprehensive(resume_text, job_description)
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        logger.info(f"Analysis completed: {analysis['skill_match_score']}% skill match")
        
        return AnalysisResponse(
            success=True,
            message="Analysis completed successfully",
            analysis=analysis,
            processing_time=round(processing_time, 3)
        )
        
    except Exception as e:
        logger.error(f"Error analyzing resume: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/match_jobs", response_model=JobMatchResponse)
async def match_jobs(file_id: str):
    """Match resume against eligible job openings only"""
    
    if file_id not in uploaded_files:
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        resume_skills = uploaded_files[file_id]["skills"]
        eligible_matches = match_jobs_realtime(resume_skills)
        
        # Calculate statistics
        total_jobs = len(REAL_COMPANY_JOBS)
        eligible_matches_count = len(eligible_matches)
        best_fit_company = eligible_matches[0].company if eligible_matches else "None"
        average_fit_score = sum(match.fit_score for match in eligible_matches) / eligible_matches_count if eligible_matches else 0
        
        logger.info(f"Job matching: {eligible_matches_count}/{total_jobs} jobs are eligible")
        
        return JobMatchResponse(
            success=True,
            matches=eligible_matches,
            total_matches=total_jobs,
            eligible_matches=eligible_matches_count,
            best_fit_company=best_fit_company,
            average_fit_score=round(average_fit_score, 1)
        )
        
    except Exception as e:
        logger.error(f"Error matching jobs: {e}")
        raise HTTPException(status_code=500, detail=f"Job matching failed: {str(e)}")

# Mount static files at the end
if Path("static").exists():
    app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    print("Starting Fixed Enhanced AI Resume Analyzer Backend")
    print("Features: Accurate skill matching, Eligible jobs only, Correct percentages")
    print("Access at: http://localhost:9002")
    uvicorn.run(app, host="0.0.0.0", port=9002)
