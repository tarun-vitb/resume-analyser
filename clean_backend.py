"""
Clean AI Resume Analyzer Backend - No Unicode Issues
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
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AI Resume Analyzer API",
    description="Clean AI-powered resume analysis",
    version="2.0.0"
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

# Mount static files at the end, after all API routes
# This will be moved to the bottom of the file

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

# Enhanced job database with more detailed information
MOCK_JOBS = [
    {
        "role_title": "Senior Python Backend Developer",
        "company": "TechSolutions Inc",
        "location": "San Francisco, CA",
        "job_type": "Full-time",
        "experience_level": "Senior (5+ years)",
        "description": "Results-driven Python Backend Developer with 5+ years of experience in designing and developing scalable web applications using Flask. Proven expertise in REST API development and integration with relational databases.",
        "skills_required": ["Python", "Flask", "REST APIs", "PostgreSQL", "MySQL", "Git", "HTML", "CSS", "JavaScript"],
        "preferred_skills": ["Docker", "AWS", "Redis", "CI/CD", "Microservices"],
        "salary_range": "$120k - $160k",
        "benefits": ["Health Insurance", "401k", "Remote Work", "Stock Options"],
        "posted_date": "2024-01-15",
        "application_deadline": "2024-02-15"
    },
    {
        "role_title": "Full Stack Developer (React + Node.js)",
        "company": "WebDev Solutions",
        "location": "New York, NY",
        "job_type": "Full-time",
        "experience_level": "Mid-level (3-5 years)",
        "description": "Seeking a full stack developer with expertise in React frontend and Node.js backend development. Experience with modern JavaScript frameworks and database management required.",
        "skills_required": ["JavaScript", "React", "Node.js", "Express", "MongoDB", "HTML", "CSS", "Git"],
        "preferred_skills": ["TypeScript", "Redux", "GraphQL", "Docker", "AWS"],
        "salary_range": "$90k - $130k",
        "benefits": ["Health Insurance", "Flexible Hours", "Learning Budget"],
        "posted_date": "2024-01-10",
        "application_deadline": "2024-02-10"
    },
    {
        "role_title": "DevOps Engineer",
        "company": "CloudTech Solutions",
        "location": "Austin, TX",
        "job_type": "Full-time",
        "experience_level": "Senior (4+ years)",
        "description": "DevOps engineer with AWS, Docker, Kubernetes experience. Responsible for CI/CD pipelines, infrastructure automation, and cloud deployment.",
        "skills_required": ["AWS", "Docker", "Kubernetes", "Jenkins", "Linux", "Python", "Terraform"],
        "preferred_skills": ["Ansible", "Prometheus", "Grafana", "ELK Stack"],
        "salary_range": "$110k - $150k",
        "benefits": ["Health Insurance", "401k", "Remote Work", "Certification Budget"],
        "posted_date": "2024-01-12",
        "application_deadline": "2024-02-12"
    },
    {
        "role_title": "Data Scientist",
        "company": "DataFlow Analytics",
        "location": "Boston, MA",
        "job_type": "Full-time",
        "experience_level": "Mid-Senior (3+ years)",
        "description": "Data scientist with strong Python, SQL, and machine learning skills. Experience with statistical analysis and data visualization required.",
        "skills_required": ["Python", "SQL", "Machine Learning", "Pandas", "NumPy", "Statistics", "Data Analysis"],
        "preferred_skills": ["TensorFlow", "PyTorch", "Tableau", "R", "Spark"],
        "salary_range": "$100k - $140k",
        "benefits": ["Health Insurance", "Research Time", "Conference Budget"],
        "posted_date": "2024-01-08",
        "application_deadline": "2024-02-08"
    },
    {
        "role_title": "Machine Learning Engineer",
        "company": "AI Innovations",
        "location": "Seattle, WA",
        "job_type": "Full-time",
        "experience_level": "Senior (5+ years)",
        "description": "ML engineer to build and deploy machine learning models. Experience with MLOps, model deployment, and cloud platforms required.",
        "skills_required": ["Python", "Machine Learning", "TensorFlow", "PyTorch", "AWS", "Docker", "MLOps"],
        "preferred_skills": ["Kubernetes", "Airflow", "Spark", "Databricks"],
        "salary_range": "$140k - $180k",
        "benefits": ["Health Insurance", "401k", "Stock Options", "GPU Access"],
        "posted_date": "2024-01-05",
        "application_deadline": "2024-02-05"
    },
    {
        "role_title": "Frontend Developer (React)",
        "company": "UI/UX Studio",
        "location": "Los Angeles, CA",
        "job_type": "Full-time",
        "experience_level": "Mid-level (2-4 years)",
        "description": "Frontend developer specializing in React applications. Strong CSS and JavaScript skills required. Experience with modern frontend tools and responsive design.",
        "skills_required": ["React", "JavaScript", "HTML", "CSS", "Git", "Responsive Design"],
        "preferred_skills": ["TypeScript", "Redux", "Sass", "Webpack", "Jest"],
        "salary_range": "$80k - $120k",
        "benefits": ["Health Insurance", "Flexible Hours", "Creative Freedom"],
        "posted_date": "2024-01-14",
        "application_deadline": "2024-02-14"
    },
    {
        "role_title": "Database Administrator",
        "company": "DataSafe Corp",
        "location": "Chicago, IL",
        "job_type": "Full-time",
        "experience_level": "Senior (4+ years)",
        "description": "Database administrator with expertise in PostgreSQL and MySQL. Experience with database optimization, backup strategies, and performance tuning.",
        "skills_required": ["PostgreSQL", "MySQL", "SQL", "Database Design", "Performance Tuning", "Backup & Recovery"],
        "preferred_skills": ["MongoDB", "Redis", "Oracle", "AWS RDS"],
        "salary_range": "$95k - $135k",
        "benefits": ["Health Insurance", "401k", "Training Budget"],
        "posted_date": "2024-01-11",
        "application_deadline": "2024-02-11"
    },
    {
        "role_title": "Software Architect",
        "company": "Enterprise Solutions",
        "location": "Dallas, TX",
        "job_type": "Full-time",
        "experience_level": "Senior (7+ years)",
        "description": "Software architect with extensive experience in system design, microservices, and cloud architecture. Leadership experience required.",
        "skills_required": ["System Design", "Microservices", "Cloud Architecture", "Leadership", "Python", "Java"],
        "preferred_skills": ["Kubernetes", "Event Sourcing", "CQRS", "Domain-Driven Design"],
        "salary_range": "$160k - $200k",
        "benefits": ["Health Insurance", "401k", "Stock Options", "Sabbatical"],
        "posted_date": "2024-01-07",
        "application_deadline": "2024-02-07"
    }
]

def extract_text_simple(file_path: str, file_extension: str) -> str:
    """Simple text extraction"""
    try:
        if file_extension == '.txt':
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        else:
            # For other formats, return a message
            return "Text extraction available for TXT files. For PDF/DOCX support, additional libraries needed."
    except Exception as e:
        return f"Error extracting text: {str(e)}"

def extract_skills_simple(text: str) -> List[str]:
    """Enhanced skill extraction with comprehensive database"""
    skills_database = [
        # Programming Languages
        "Python", "JavaScript", "Java", "C++", "C#", "Go", "Rust", "PHP", "Ruby", "Swift",
        "Kotlin", "TypeScript", "R", "Scala", "MATLAB", "Perl", "Shell", "Bash",
        
        # Web Technologies & Frameworks
        "React", "Angular", "Vue.js", "Node.js", "Express", "Django", "Flask", "FastAPI",
        "Spring", "Laravel", "Rails", "ASP.NET", "jQuery", "Bootstrap", "Tailwind",
        "Sass", "Less", "Webpack", "Vite", "Next.js", "Nuxt.js", "Svelte",
        
        # Databases
        "SQL", "MySQL", "PostgreSQL", "MongoDB", "Redis", "Elasticsearch", "SQLite",
        "Oracle", "Cassandra", "DynamoDB", "Neo4j", "InfluxDB", "CouchDB",
        
        # Cloud & DevOps
        "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Jenkins", "GitLab", "GitHub",
        "Terraform", "Ansible", "Chef", "Puppet", "Vagrant", "CI/CD", "DevOps",
        "Microservices", "Serverless", "Lambda", "EC2", "S3", "RDS",
        
        # Data Science & ML
        "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Scikit-learn",
        "Pandas", "NumPy", "Matplotlib", "Seaborn", "Jupyter", "Statistics", 
        "Data Analysis", "Big Data", "Spark", "Hadoop", "Tableau", "Power BI",
        "MLOps", "Airflow", "Databricks", "Kafka", "ETL",
        
        # Mobile Development
        "iOS", "Android", "React Native", "Flutter", "Xamarin", "Ionic",
        
        # Testing & Quality
        "Unit Testing", "Integration Testing", "Jest", "Pytest", "Selenium", "Cypress",
        "Test Automation", "TDD", "BDD", "Quality Assurance",
        
        # Tools & Technologies
        "Git", "SVN", "Linux", "Unix", "Windows", "MacOS", "Vim", "VS Code",
        "IntelliJ", "Eclipse", "Postman", "Swagger", "REST APIs", "GraphQL",
        "JSON", "XML", "YAML", "Markdown",
        
        # Soft Skills & Methodologies
        "Agile", "Scrum", "Kanban", "Leadership", "Team Management", "Project Management",
        "Communication", "Problem Solving", "Critical Thinking", "Mentoring",
        
        # Web Technologies
        "HTML", "CSS", "SCSS", "Responsive Design", "Progressive Web Apps", "PWA",
        "Single Page Applications", "SPA", "Server-Side Rendering", "SSR",
        
        # Security
        "Cybersecurity", "Penetration Testing", "OAuth", "JWT", "SSL", "TLS",
        "Encryption", "HTTPS", "Security Auditing",
        
        # Business & Analytics
        "Business Analysis", "Requirements Gathering", "Stakeholder Management",
        "Data Visualization", "Reporting", "KPI", "Metrics", "Analytics"
    ]
    
    found_skills = []
    text_lower = text.lower()
    
    # Enhanced pattern matching
    for skill in skills_database:
        # Check for exact match with word boundaries
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.append(skill)
        
        # Check for common variations
        skill_variations = {
            "JavaScript": ["js", "javascript", "ecmascript"],
            "TypeScript": ["ts", "typescript"],
            "Python": ["python3", "py"],
            "PostgreSQL": ["postgres", "psql"],
            "MongoDB": ["mongo"],
            "Machine Learning": ["ml", "machine learning", "artificial intelligence", "ai"],
            "Deep Learning": ["dl", "neural networks"],
            "REST APIs": ["rest", "restful", "api", "apis"],
            "CI/CD": ["continuous integration", "continuous deployment", "cicd"],
            "HTML": ["html5"],
            "CSS": ["css3"],
            "Node.js": ["nodejs", "node"],
            "React": ["reactjs", "react.js"],
            "Vue.js": ["vuejs", "vue"]
        }
        
        if skill in skill_variations:
            for variation in skill_variations[skill]:
                if re.search(r'\b' + re.escape(variation) + r'\b', text_lower):
                    if skill not in found_skills:
                        found_skills.append(skill)
    
    return list(set(found_skills))

def calculate_similarity_simple(text1: str, text2: str) -> float:
    """Simple similarity calculation"""
    words1 = set(re.findall(r'\w+', text1.lower()))
    words2 = set(re.findall(r'\w+', text2.lower()))
    
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    if len(union) == 0:
        return 0.0
    
    return len(intersection) / len(union)

def analyze_resume_enhanced(resume_text: str, job_description: str) -> Dict[str, Any]:
    """Enhanced resume analysis with detailed skill matching"""
    
    resume_skills = extract_skills_simple(resume_text)
    job_skills = extract_skills_simple(job_description)
    
    # Categorize skills
    skill_categories = {
        "Programming Languages": ["Python", "JavaScript", "Java", "C++", "C#", "Go", "Rust", "PHP", "Ruby", "TypeScript"],
        "Web Technologies": ["React", "Angular", "Vue.js", "Node.js", "Express", "Django", "Flask", "HTML", "CSS"],
        "Databases": ["SQL", "MySQL", "PostgreSQL", "MongoDB", "Redis", "Oracle", "SQLite"],
        "Cloud & DevOps": ["AWS", "Azure", "GCP", "Docker", "Kubernetes", "Jenkins", "CI/CD", "Terraform"],
        "Data Science": ["Machine Learning", "TensorFlow", "PyTorch", "Pandas", "NumPy", "Statistics", "Data Analysis"],
        "Tools & Frameworks": ["Git", "Linux", "REST APIs", "GraphQL", "Agile", "Scrum"]
    }
    
    # Match skills by category
    matched_skills = list(set(resume_skills).intersection(set(job_skills)))
    missing_skills = list(set(job_skills) - set(resume_skills))
    extra_skills = list(set(resume_skills) - set(job_skills))
    
    # Calculate weighted scores
    critical_skills = job_skills[:5]  # First 5 skills are considered critical
    critical_matched = [skill for skill in matched_skills if skill in critical_skills]
    critical_missing = [skill for skill in missing_skills if skill in critical_skills]
    
    # Enhanced scoring algorithm
    skill_match_score = len(matched_skills) / len(job_skills) if job_skills else 0
    critical_skill_score = len(critical_matched) / len(critical_skills) if critical_skills else 0
    semantic_similarity = calculate_similarity_simple(resume_text, job_description)
    
    # Experience level detection
    experience_keywords = ["years", "experience", "senior", "lead", "manager", "architect"]
    experience_mentions = sum(1 for keyword in experience_keywords if keyword in resume_text.lower())
    experience_score = min(experience_mentions / 3, 1.0)
    
    # Calculate comprehensive fit score
    fit_score = (
        semantic_similarity * 0.25 +
        skill_match_score * 0.35 +
        critical_skill_score * 0.25 +
        experience_score * 0.15
    ) * 100
    
    # More accurate selection probability
    selection_probability = min(fit_score * 0.9 + 10, 95)
    
    # Enhanced feedback generation
    feedback = []
    if fit_score < 40:
        feedback.append("Your resume needs significant improvement to match this role")
    elif fit_score < 60:
        feedback.append("Good foundation, but consider adding more relevant skills and experience")
    elif fit_score < 80:
        feedback.append("Strong candidate! Focus on highlighting key achievements")
    else:
        feedback.append("Excellent match! Your profile aligns well with the job requirements")
    
    if len(critical_missing) > 0:
        feedback.append(f"Critical missing skills: {', '.join(critical_missing[:3])}")
    
    if len(matched_skills) < 3:
        feedback.append("Include more technical skills that match the job requirements")
    
    if experience_score < 0.3:
        feedback.append("Add more details about your work experience and achievements")
    
    if len(resume_text.split()) < 200:
        feedback.append("Expand your resume with more detailed descriptions of your projects")
    
    # Categorized skill analysis
    skill_analysis = {}
    for category, category_skills in skill_categories.items():
        category_resume_skills = [skill for skill in resume_skills if skill in category_skills]
        category_job_skills = [skill for skill in job_skills if skill in category_skills]
        category_matched = [skill for skill in matched_skills if skill in category_skills]
        
        if category_job_skills:
            skill_analysis[category] = {
                "required": category_job_skills,
                "matched": category_matched,
                "missing": [skill for skill in category_job_skills if skill not in category_matched],
                "match_percentage": round((len(category_matched) / len(category_job_skills)) * 100, 1) if category_job_skills else 0
            }
    
    # Enhanced course recommendations
    course_recommendations = []
    priority_skills = critical_missing + missing_skills[:3]
    
    course_database = {
        "Python": {"provider": "Coursera", "duration": "6 weeks", "rating": 4.8, "price": "$49"},
        "JavaScript": {"provider": "Udemy", "duration": "8 weeks", "rating": 4.7, "price": "$39"},
        "React": {"provider": "Pluralsight", "duration": "4 weeks", "rating": 4.6, "price": "$29"},
        "AWS": {"provider": "AWS Training", "duration": "10 weeks", "rating": 4.9, "price": "$99"},
        "Docker": {"provider": "Docker", "duration": "3 weeks", "rating": 4.5, "price": "$35"},
        "Machine Learning": {"provider": "Coursera", "duration": "12 weeks", "rating": 4.8, "price": "$79"},
        "SQL": {"provider": "Codecademy", "duration": "5 weeks", "rating": 4.4, "price": "$25"},
        "Node.js": {"provider": "Udemy", "duration": "6 weeks", "rating": 4.6, "price": "$45"}
    }
    
    for skill in priority_skills[:5]:
        if skill in course_database:
            course_info = course_database[skill]
            course_recommendations.append({
                "skill": skill,
                "course_title": f"Master {skill} - Complete Guide",
                "provider": course_info["provider"],
                "duration": course_info["duration"],
                "rating": course_info["rating"],
                "price": course_info["price"],
                "priority": "High" if skill in critical_missing else "Medium"
            })
        else:
            course_recommendations.append({
                "skill": skill,
                "course_title": f"Complete {skill} Course",
                "provider": "Coursera" if len(skill) % 2 == 0 else "Udemy",
                "duration": f"{3 + len(skill) % 6} weeks",
                "rating": round(4.0 + (len(skill) % 10) * 0.1, 1),
                "price": f"${25 + len(skill) % 75}",
                "priority": "High" if skill in critical_missing else "Medium"
            })
    
    return {
        "fit_score": round(fit_score, 2),
        "selection_probability": round(selection_probability, 1),
        "semantic_similarity": round(semantic_similarity * 100, 1),
        "skill_match_score": round(skill_match_score * 100, 1),
        "critical_skill_score": round(critical_skill_score * 100, 1),
        "experience_score": round(experience_score * 100, 1),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "critical_missing_skills": critical_missing,
        "extra_skills": extra_skills[:10],  # Limit to top 10
        "total_skills_found": len(resume_skills),
        "total_job_skills": len(job_skills),
        "skill_analysis": skill_analysis,
        "feedback": feedback,
        "course_recommendations": course_recommendations,
        "resume_stats": {
            "word_count": len(resume_text.split()),
            "character_count": len(resume_text),
            "experience_mentions": experience_mentions,
            "sections_detected": len([s for s in ["experience", "education", "skills", "projects", "certifications"] 
                                    if s in resume_text.lower()])
        }
    }

@app.get("/api")
async def api_root():
    """API root endpoint"""
    return {"message": "AI Resume Analyzer API", "status": "running"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/upload_resume", response_model=UploadResponse)
async def upload_resume(file: UploadFile = File(...)):
    """Upload and process resume file"""
    
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
        
        uploaded_files[file_id] = {
            "filename": file.filename,
            "file_path": str(file_path),
            "extracted_text": extracted_text,
            "upload_time": datetime.now().isoformat(),
            "file_size": os.path.getsize(file_path)
        }
        
        skills = extract_skills_simple(extracted_text)
        
        return UploadResponse(
            success=True,
            message="Resume uploaded successfully",
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
    job_description: str = Form(...)
):
    """Analyze resume against job description"""
    
    import time
    start_time = time.time()
    
    if file_id not in uploaded_files:
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        resume_text = uploaded_files[file_id]["extracted_text"]
        analysis = analyze_resume_enhanced(resume_text, job_description)
        processing_time = time.time() - start_time
        
        return AnalysisResponse(
            success=True,
            message="Analysis completed successfully",
            analysis=analysis,
            processing_time=round(processing_time, 2)
        )
        
    except Exception as e:
        logger.error(f"Error analyzing resume: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/match_jobs", response_model=JobMatchResponse)
async def match_jobs(file_id: str):
    """Match resume against job positions"""
    
    if file_id not in uploaded_files:
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        resume_text = uploaded_files[file_id]["extracted_text"]
        resume_skills = extract_skills_simple(resume_text)
        
        matches = []
        
        # Experience level detection from resume
        experience_keywords = {
            "senior": 3, "lead": 4, "manager": 5, "architect": 6, "director": 7,
            "years": 1, "experience": 1, "worked": 1, "developed": 1
        }
        resume_experience_score = 0
        for keyword, weight in experience_keywords.items():
            if keyword in resume_text.lower():
                resume_experience_score += weight
        
        resume_experience_level = min(resume_experience_score / 10, 1.0)
        
        for job in MOCK_JOBS:
            # Enhanced skill matching
            required_skills = job["skills_required"]
            preferred_skills = job.get("preferred_skills", [])
            all_job_skills = required_skills + preferred_skills
            
            matched_required = list(set(resume_skills).intersection(set(required_skills)))
            matched_preferred = list(set(resume_skills).intersection(set(preferred_skills)))
            matched_skills = matched_required + matched_preferred
            
            missing_required = list(set(required_skills) - set(resume_skills))
            missing_preferred = list(set(preferred_skills) - set(resume_skills))
            missing_skills = missing_required + missing_preferred
            
            # Calculate weighted scores
            required_match_score = len(matched_required) / len(required_skills) if required_skills else 0
            preferred_match_score = len(matched_preferred) / len(preferred_skills) if preferred_skills else 0
            
            # Semantic similarity with job description
            semantic_similarity = calculate_similarity_simple(resume_text, job["description"])
            
            # Experience level matching
            job_exp_level = 0.5  # Default mid-level
            if "senior" in job["experience_level"].lower() or "5+" in job["experience_level"]:
                job_exp_level = 0.8
            elif "mid" in job["experience_level"].lower():
                job_exp_level = 0.6
            elif "junior" in job["experience_level"].lower():
                job_exp_level = 0.3
            
            experience_match = 1 - abs(resume_experience_level - job_exp_level)
            
            # Comprehensive fit score calculation
            fit_score = (
                required_match_score * 0.4 +      # Required skills (40%)
                preferred_match_score * 0.2 +     # Preferred skills (20%)
                semantic_similarity * 0.25 +      # Content similarity (25%)
                experience_match * 0.15           # Experience match (15%)
            ) * 100
            
            # More realistic selection probability
            base_probability = fit_score * 0.8
            if len(missing_required) == 0:
                base_probability += 15  # Bonus for having all required skills
            elif len(missing_required) <= 2:
                base_probability += 10  # Small bonus for missing few required skills
            
            selection_probability = min(base_probability, 95)
            
            # Enhanced match details
            match_details = {
                "role_title": job["role_title"],
                "company": job["company"],
                "location": job.get("location", "Not specified"),
                "job_type": job.get("job_type", "Full-time"),
                "experience_level": job.get("experience_level", "Not specified"),
                "fit_score": round(fit_score, 1),
                "skills_overlap": matched_skills,
                "missing_skills": missing_skills[:8],  # Show more missing skills
                "missing_required": missing_required,
                "missing_preferred": missing_preferred,
                "selection_probability": round(selection_probability, 1),
                "salary_range": job.get("salary_range", "Not specified"),
                "benefits": job.get("benefits", []),
                "posted_date": job.get("posted_date", "Recently"),
                "application_deadline": job.get("application_deadline", "Open"),
                "match_breakdown": {
                    "required_skills_match": round(required_match_score * 100, 1),
                    "preferred_skills_match": round(preferred_match_score * 100, 1),
                    "content_similarity": round(semantic_similarity * 100, 1),
                    "experience_match": round(experience_match * 100, 1)
                }
            }
            
            matches.append(JobMatch(
                role_title=match_details["role_title"],
                company=match_details["company"],
                fit_score=match_details["fit_score"],
                skills_overlap=match_details["skills_overlap"],
                missing_skills=match_details["missing_skills"],
                selection_probability=match_details["selection_probability"],
                salary_range=match_details["salary_range"]
            ))
        
        # Sort by fit score and then by selection probability
        matches.sort(key=lambda x: (x.fit_score, x.selection_probability), reverse=True)
        
        return JobMatchResponse(
            success=True,
            matches=matches,
            total_matches=len(matches)
        )
        
    except Exception as e:
        logger.error(f"Error matching jobs: {e}")
        raise HTTPException(status_code=500, detail=f"Job matching failed: {str(e)}")

# Mount static files after all API routes are defined
if Path("static").exists():
    app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    print("Starting AI Resume Analyzer Backend")
    print("Server: http://localhost:9000")
    print("API Docs: http://localhost:9000/docs")
    
    uvicorn.run(
        "clean_backend:app",
        host="0.0.0.0",
        port=9000,
        reload=True,
        log_level="info"
    )
