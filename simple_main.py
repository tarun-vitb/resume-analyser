"""
Simplified AI Resume Analyzer - Quick Start Version
Fixed all common errors and dependencies for immediate local running
"""

import os
import logging
import tempfile
import shutil
from typing import List, Dict, Any, Optional
from pathlib import Path

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
    title="AI Resume Analyzer",
    description="Simplified AI-powered resume analysis",
    version="1.0.0"
)

# Add CORS middleware
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

# Simple response models
class AnalysisResponse(BaseModel):
    success: bool
    message: str
    data: Dict[str, Any]

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Resume Analyzer API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "upload": "/api/v1/upload-resume",
            "analyze": "/api/v1/analyze-resume-simple"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "AI Resume Analyzer is running"}

@app.post("/api/v1/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """Simple resume upload and text extraction"""
    
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
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
            shutil.copyfileobj(file.file, tmp_file)
            tmp_path = tmp_file.name
        
        # Simple text extraction
        extracted_text = ""
        file_size = os.path.getsize(tmp_path)
        
        if file_extension == '.txt':
            with open(tmp_path, 'r', encoding='utf-8') as f:
                extracted_text = f.read()
        elif file_extension == '.pdf':
            try:
                import PyPDF2
                with open(tmp_path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    for page in reader.pages:
                        extracted_text += page.extract_text()
            except ImportError:
                extracted_text = "PDF processing requires PyPDF2. Install with: pip install PyPDF2"
        elif file_extension in ['.docx', '.doc']:
            try:
                from docx import Document
                doc = Document(tmp_path)
                extracted_text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
            except ImportError:
                extracted_text = "DOCX processing requires python-docx. Install with: pip install python-docx"
        
        # Clean up temporary file
        os.unlink(tmp_path)
        
        # Simple analysis
        word_count = len(extracted_text.split())
        char_count = len(extracted_text)
        
        return AnalysisResponse(
            success=True,
            message="Resume uploaded and processed successfully",
            data={
                "filename": file.filename,
                "file_size": file_size,
                "extracted_text": extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text,
                "word_count": word_count,
                "character_count": char_count,
                "file_type": file_extension
            }
        )
        
    except Exception as e:
        # Clean up temporary file if it exists
        if 'tmp_path' in locals():
            try:
                os.unlink(tmp_path)
            except:
                pass
        
        logger.error(f"Error processing resume: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing resume: {str(e)}")

@app.post("/api/v1/analyze-resume-simple")
async def analyze_resume_simple(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    """Simple resume analysis against job description"""
    
    try:
        # Upload and extract text
        upload_result = await upload_resume(file)
        extracted_text = upload_result.data.get("extracted_text", "")
        
        # Simple keyword matching
        job_keywords = set(job_description.lower().split())
        resume_keywords = set(extracted_text.lower().split())
        
        # Find matching keywords
        matching_keywords = job_keywords.intersection(resume_keywords)
        match_percentage = (len(matching_keywords) / len(job_keywords)) * 100 if job_keywords else 0
        
        # Simple skill extraction (basic keywords)
        common_skills = [
            'python', 'java', 'javascript', 'react', 'node', 'sql', 'html', 'css',
            'aws', 'docker', 'kubernetes', 'git', 'linux', 'machine learning',
            'data analysis', 'project management', 'communication', 'leadership'
        ]
        
        found_skills = []
        for skill in common_skills:
            if skill in extracted_text.lower():
                found_skills.append(skill.title())
        
        # Simple recommendations
        recommendations = []
        if match_percentage < 30:
            recommendations.append("Consider adding more relevant keywords from the job description")
        if len(found_skills) < 5:
            recommendations.append("Add more technical skills to your resume")
        if len(extracted_text.split()) < 200:
            recommendations.append("Consider expanding your resume with more details")
        
        return AnalysisResponse(
            success=True,
            message="Resume analysis completed",
            data={
                "match_percentage": round(match_percentage, 2),
                "matching_keywords": list(matching_keywords)[:10],
                "found_skills": found_skills,
                "recommendations": recommendations,
                "resume_stats": {
                    "word_count": len(extracted_text.split()),
                    "character_count": len(extracted_text)
                }
            }
        )
        
    except Exception as e:
        logger.error(f"Error in resume analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/api/v1/demo")
async def demo_analysis():
    """Demo endpoint with sample data"""
    return {
        "demo_analysis": {
            "match_percentage": 75.5,
            "found_skills": ["Python", "JavaScript", "React", "SQL", "Git"],
            "recommendations": [
                "Add more cloud computing skills like AWS or Azure",
                "Include specific project examples",
                "Quantify your achievements with numbers"
            ],
            "sample_feedback": {
                "strengths": ["Strong technical skills", "Good project experience"],
                "improvements": ["Add more soft skills", "Include certifications"]
            }
        }
    }

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "data": {}
        }
    )

if __name__ == "__main__":
    print("🚀 Starting AI Resume Analyzer (Simplified Version)")
    print("📍 Server will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("💚 Health Check: http://localhost:8000/health")
    print("🎯 Demo Endpoint: http://localhost:8000/api/v1/demo")
    
    uvicorn.run(
        "simple_main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
