"""
FastAPI Backend for AI Resume Analyzer
Production-ready API with comprehensive resume analysis capabilities
"""

import os
import logging
import asyncio
from typing import List, Dict, Any, Optional
from pathlib import Path
import tempfile
import shutil

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
import uvicorn

# Import our core modules
from core.document_processor import DocumentProcessor, ExtractedData
from core.nlp_engine import NLPEngine
from core.prediction_model import SelectionPredictor, PredictionFeatures
from core.skill_analyzer import SkillAnalyzer, SkillGapAnalysis
from core.upskilling_engine import UpskillingEngine, UpskillingPlan
from core.feedback_generator import FeedbackGenerator, ResumeAnalysis
from core.role_matcher import RoleMatcher, RoleMatchingResults

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Pydantic models for API requests/responses
class JobDescription(BaseModel):
    job_id: Optional[str] = None
    title: str
    company: str
    description: str
    location: Optional[str] = None
    salary_range: Optional[str] = None

class AnalysisRequest(BaseModel):
    job_description: str
    target_role: Optional[str] = None
    analysis_type: str = Field(default="comprehensive", description="Type of analysis: basic, comprehensive, or detailed")

class MultiJobAnalysisRequest(BaseModel):
    job_descriptions: List[JobDescription]
    prioritize_by: str = Field(default="match_score", description="Prioritization criteria: match_score, selection_probability, or skill_overlap")

class AnalysisResponse(BaseModel):
    success: bool
    message: str
    data: Dict[str, Any]
    processing_time: float

class HealthResponse(BaseModel):
    status: str
    version: str
    components: Dict[str, str]

# Initialize FastAPI app
app = FastAPI(
    title="AI Resume Analyzer API",
    description="Advanced AI-powered resume analysis and job matching platform",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174", "http://localhost:5173", "http://localhost:3000"],  # Frontend development servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for core components
document_processor = None
nlp_engine = None
prediction_model = None
skill_analyzer = None
upskilling_engine = None
feedback_generator = None
role_matcher = None

# Global storage for uploaded resume data (session-based)
uploaded_resume_data = {}

# Create necessary directories
UPLOAD_DIR = Path("uploads")
CACHE_DIR = Path("cache")
UPLOAD_DIR.mkdir(exist_ok=True)
CACHE_DIR.mkdir(exist_ok=True)

@app.on_event("startup")
async def startup_event():
    """Initialize all core components on startup"""
    global document_processor, nlp_engine, prediction_model, skill_analyzer
    global upskilling_engine, feedback_generator, role_matcher
    
    logger.info("Initializing AI Resume Analyzer components...")
    
    try:
        # Initialize core components
        document_processor = DocumentProcessor()
        logger.info("✓ Document processor initialized")
        
        nlp_engine = NLPEngine(cache_embeddings=True)
        logger.info("✓ NLP engine initialized")
        
        prediction_model = SelectionPredictor(model_type="xgboost")
        # Train with synthetic data for demo
        prediction_model.train_model()
        logger.info("✓ Prediction model initialized and trained")
        
        skill_analyzer = SkillAnalyzer()
        logger.info("✓ Skill analyzer initialized")
        
        upskilling_engine = UpskillingEngine()
        logger.info("✓ Upskilling engine initialized")
        
        feedback_generator = FeedbackGenerator()
        logger.info("✓ Feedback generator initialized")
        
        role_matcher = RoleMatcher(nlp_engine, skill_analyzer, prediction_model)
        logger.info("✓ Role matcher initialized")
        
        logger.info("🚀 All components initialized successfully!")
        
    except Exception as e:
        logger.error(f"Failed to initialize components: {e}")
        raise

@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint with system health information"""
    return HealthResponse(
        status="healthy",
        version="2.0.0",
        components={
            "document_processor": "ready" if document_processor else "not_ready",
            "nlp_engine": "ready" if nlp_engine else "not_ready",
            "prediction_model": "ready" if prediction_model else "not_ready",
            "skill_analyzer": "ready" if skill_analyzer else "not_ready",
            "upskilling_engine": "ready" if upskilling_engine else "not_ready",
            "feedback_generator": "ready" if feedback_generator else "not_ready",
            "role_matcher": "ready" if role_matcher else "not_ready"
        }
    )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}

@app.post("/api/v1/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """Upload and extract text from resume file"""
    
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Validate file type
    allowed_extensions = {'.pdf', '.docx', '.doc'}
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
        
        # Extract structured data
        extracted_data = document_processor.extract_structured_data(tmp_path)
        
        # Validate extraction quality
        validation = document_processor.validate_extraction(extracted_data)
        
        # Clean up temporary file
        os.unlink(tmp_path)
        
        # Store resume data globally for company-matches endpoint
        global uploaded_resume_data
        uploaded_resume_data = {
            "name": extracted_data.name or "Unknown",
            "email": extracted_data.email or "Not specified",
            "phone": extracted_data.phone or "Not specified",
            "skills": extracted_data.skills or [],
            "experience": extracted_data.experience or [],
            "education": extracted_data.education or [],
            "cleaned_text": extracted_data.cleaned_text
        }
        
        # Ensure skills is a list and not empty
        skills_list = extracted_data.skills if extracted_data.skills else []
        logger.info(f"Extracted {len(skills_list)} skills: {skills_list[:10]}")
        
        # Return format expected by frontend
        response_data = {
            "success": True,
            "message": "Resume uploaded and processed successfully",
            "name": extracted_data.name or "Unknown",
            "email": extracted_data.email or "Not specified",
            "phone": extracted_data.phone or "Not specified",
            "skills": skills_list,  # Always a list
            "experience": extracted_data.experience or [],
            "education": extracted_data.education or [],
            "word_count": len(extracted_data.cleaned_text.split()),
            "validation": validation
        }
        
        logger.info(f"Upload response: skills count = {len(response_data['skills'])}")
        return response_data
        
    except Exception as e:
        # Clean up temporary file if it exists
        if 'tmp_path' in locals():
            try:
                os.unlink(tmp_path)
            except:
                pass
        
        logger.error(f"Error processing resume: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing resume: {str(e)}")

@app.post("/api/v1/analyze-resume")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...),
    target_role: Optional[str] = Form(None),
    analysis_type: Optional[str] = Form("comprehensive")
):
    """Comprehensive resume analysis against job description"""
    
    import time
    start_time = time.time()
        
    try:
        logger.info(f"Analyzing resume: {file.filename}")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp_file:
            shutil.copyfileobj(file.file, tmp_file)
            tmp_path = tmp_file.name
        
        try:
            # Extract data from resume
            extracted_data = document_processor.extract_structured_data(tmp_path)
            
            # Prepare resume data dictionary
            resume_data = {
                'cleaned_text': extracted_data.cleaned_text,
                'name': extracted_data.name,
                'email': extracted_data.email,
                'phone': extracted_data.phone,
                'skills': extracted_data.skills,
                'experience': extracted_data.experience,
                'education': extracted_data.education,
                'sections': extracted_data.sections
            }
            
            # 1. Semantic Similarity Analysis
            semantic_similarity = nlp_engine.compute_semantic_similarity(
                extracted_data.cleaned_text, job_description
            )
            
            # 2. Skill Gap Analysis
            skill_analysis = skill_analyzer.analyze_skill_gaps(
                extracted_data.cleaned_text, job_description, extracted_data.skills
            )
            
            matched_skills_list = [s.skill for s in skill_analysis.matched_skills]
            missing_skills_list = [s.skill for s in skill_analysis.missing_skills]
            
            # 3. Selection Probability Prediction
            prediction_features = prediction_model.extract_features(
                resume_data, job_description, semantic_similarity, {
                    'matched_skills': matched_skills_list,
                    'missing_skills': missing_skills_list
                }
            )
            selection_probability = prediction_model.predict_selection_probability(prediction_features)
            
            # Calculate fit_score (0-100) from match score
            fit_score = int(skill_analysis.overall_match_score * 100)
            shortlist_probability = int(selection_probability * 100)
            
            # 4. Generate feedback text
            feedback_parts = []
            if matched_skills_list:
                feedback_parts.append(f"You have {len(matched_skills_list)} matching skills")
            if skill_analysis.recommendations:
                feedback_parts.append(f"Recommendations: {', '.join(skill_analysis.recommendations[:2])}")
            
            feedback_text = ". ".join(feedback_parts) if feedback_parts else "Your resume shows good alignment with the job requirements."
            
            # 5. Get upskilling recommendations (courses) - Always include if missing skills exist
            recommended_courses = []
            if missing_skills_list:
                try:
                    missing_skills_top = missing_skills_list[:5]
                    skill_importance_map = {s.skill: s.importance for s in skill_analysis.missing_skills}
                    
                    upskilling_plan = upskilling_engine.create_upskilling_plan(
                        missing_skills_top, selection_probability, skill_importance_map
                    )
                    
                    # Extract courses from upskilling plan
                    for sim in upskilling_plan.skill_simulations[:3]:
                        for course in sim.recommended_courses[:2]:
                            recommended_courses.append({
                                'name': course.title if hasattr(course, 'title') else str(course),
                                'link': course.url if hasattr(course, 'url') else '#',
                                'provider': course.provider if hasattr(course, 'provider') else 'Online',
                                'duration': course.duration if hasattr(course, 'duration') else 'Self-paced'
                            })
                except Exception as e:
                    logger.warning(f"Error generating upskilling courses: {e}")
                    # Provide fallback courses based on missing skills
                    for skill in missing_skills_list[:3]:
                        recommended_courses.append({
                            'name': f'Learn {skill}',
                            'link': '#',
                            'provider': 'Various Platforms',
                            'duration': '4-8 weeks'
                        })
            
            # 6. Generate eligible jobs - Always include recommendations
            eligible_jobs = []
            try:
                # Generate job suggestions based on skills
                if matched_skills_list:
                    eligible_jobs = [
                        {
                            'title': 'Software Engineer',
                            'description': f'Looking for candidates with strong skills in {", ".join(matched_skills_list[:3])}',
                            'fit_score': min(95, fit_score + 5),
                            'salary_range': '$80K - $120K',
                            'experience_level': 'Mid-level',
                            'skills_coverage': {
                                'required': f"{len(matched_skills_list)}/{len(matched_skills_list) + len(missing_skills_list)}",
                                'preferred': f"{min(8, len(matched_skills_list))}/10"
                            },
                            'matching_skills': {
                                'required': matched_skills_list[:5],
                                'preferred': matched_skills_list[5:8] if len(matched_skills_list) > 5 else []
                            }
                        }
                    ]
            except Exception as e:
                logger.warning(f"Error generating eligible jobs: {e}")
            
            processing_time = time.time() - start_time
            
            # Ensure all lists are not None
            matched_skills_list = matched_skills_list or []
            missing_skills_list = missing_skills_list or []
            recommended_courses = recommended_courses or []
            eligible_jobs = eligible_jobs or []
            
            logger.info(f"Analysis complete - fit_score: {fit_score}, skills: {len(matched_skills_list)}, missing: {len(missing_skills_list)}")
            
            # Return format expected by frontend
            response_data = {
                "success": True,
                "message": "Analysis completed successfully",
                "fit_score": fit_score,
                "shortlist_probability": shortlist_probability,
                "skills": matched_skills_list,
                "missing_skills": missing_skills_list,
                "feedback": feedback_text,
                "recommended_courses": recommended_courses,
                "eligible_jobs": eligible_jobs,
                "processing_time": processing_time
            }
            
            logger.info(f"Returning analysis: fit_score={fit_score}, courses={len(recommended_courses)}, jobs={len(eligible_jobs)}")
            return response_data
            
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
                
    except Exception as e:
        logger.error(f"Error in resume analysis: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze resume: {str(e)}"
        )

@app.post("/api/v1/match-multiple-jobs")
async def match_multiple_jobs(
    file: UploadFile = File(...),
    request_data: str = Form(...)  # JSON string of MultiJobAnalysisRequest
):
    """Match resume against multiple job descriptions"""
    
    import json
    import time
    start_time = time.time()
    
    try:
        # Parse request data
        request_obj = json.loads(request_data)
        job_descriptions = [
            {
                'job_id': job.get('job_id', f"job_{i}"),
                'title': job['title'],
                'company': job['company'],
                'description': job['description']
            }
            for i, job in enumerate(request_obj['job_descriptions'])
        ]
        prioritize_by = request_obj.get('prioritize_by', 'match_score')
        
        # Extract resume data
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp_file:
            shutil.copyfileobj(file.file, tmp_file)
            tmp_path = tmp_file.name
        
        extracted_data = document_processor.extract_structured_data(tmp_path)
        os.unlink(tmp_path)
        
        resume_data = {
            'cleaned_text': extracted_data.cleaned_text,
            'name': extracted_data.name,
            'email': extracted_data.email,
            'phone': extracted_data.phone,
            'skills': extracted_data.skills,
            'experience': extracted_data.experience,
            'education': extracted_data.education,
            'sections': extracted_data.sections
        }
        
        # Perform role matching analysis
        matching_results = role_matcher.analyze_multiple_jobs(
            resume_data, job_descriptions, prioritize_by
        )
        
        # Format results
        results = {
            'total_jobs_analyzed': matching_results.total_jobs_analyzed,
            'match_distribution': matching_results.match_distribution,
            'career_insights': matching_results.career_insights,
            'recommended_actions': matching_results.recommended_actions,
            'top_matches': [
                {
                    'job_id': match.job_id,
                    'job_title': match.job_title,
                    'company': match.company,
                    'match_score': match.match_score,
                    'selection_probability': match.selection_probability,
                    'skill_overlap': match.skill_overlap,
                    'missing_skills': match.missing_skills[:5],
                    'matched_skills': match.matched_skills[:10],
                    'recommendation': match.recommendation,
                    'priority_level': match.priority_level
                }
                for match in matching_results.best_matches[:10]
            ],
            'skill_gap_summary': dict(list(matching_results.skill_gap_summary.items())[:10])
        }
        
        processing_time = time.time() - start_time
        
        return AnalysisResponse(
            success=True,
            message=f"Successfully analyzed resume against {len(job_descriptions)} job descriptions",
            data=results,
            processing_time=processing_time
        )
        
    except Exception as e:
        logger.error(f"Error in multi-job analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Multi-job analysis failed: {str(e)}")

@app.post("/api/v1/get-upskilling-plan")
async def get_upskilling_plan(
    missing_skills: List[str],
    current_probability: float = 0.5,
    time_constraint: Optional[int] = None
):
    """Get detailed upskilling plan for specific skills"""
    
    try:
        # Create skill importance map (assume equal importance)
        skill_importance_map = {skill: 0.8 for skill in missing_skills}
        
        # Generate upskilling plan
        plan = upskilling_engine.create_upskilling_plan(
            missing_skills, current_probability, skill_importance_map, time_constraint
        )
        
        # Format detailed response
        results = {
            'prioritized_skills': plan.prioritized_skills,
            'quick_wins': plan.quick_wins,
            'long_term_goals': plan.long_term_goals,
            'time_estimate': plan.total_time_estimate,
            'budget_estimate': plan.budget_estimate,
            'detailed_simulations': [
                {
                    'skill': sim.skill,
                    'current_probability': sim.current_probability,
                    'projected_probability': sim.projected_probability,
                    'probability_increase': sim.probability_increase,
                    'time_to_acquire': sim.time_to_acquire,
                    'difficulty_level': sim.difficulty_level,
                    'roi_score': sim.roi_score,
                    'learning_path': sim.learning_path,
                    'recommended_courses': [
                        {
                            'title': course.title,
                            'provider': course.provider,
                            'url': course.url,
                            'duration': course.duration,
                            'difficulty': course.difficulty,
                            'rating': course.rating,
                            'price': course.price,
                            'skills_covered': course.skills_covered,
                            'relevance_score': course.relevance_score
                        }
                        for course in sim.recommended_courses
                    ]
                }
                for sim in plan.skill_simulations
            ]
        }
        
        return AnalysisResponse(
            success=True,
            message="Upskilling plan generated successfully",
            data=results,
            processing_time=0.0
        )
        
    except Exception as e:
        logger.error(f"Error generating upskilling plan: {e}")
        raise HTTPException(status_code=500, detail=f"Upskilling plan generation failed: {str(e)}")

@app.get("/api/v1/skill-alternatives/{skill}")
async def get_skill_alternatives(skill: str):
    """Get alternative skills for a given skill"""
    
    try:
        alternatives = upskilling_engine.get_skill_alternatives(skill)
        learning_path = upskilling_engine.get_skill_learning_path(skill)
        
        return {
            'skill': skill,
            'alternatives': alternatives,
            'learning_path': learning_path
        }
        
    except Exception as e:
        logger.error(f"Error getting skill alternatives: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/model-info")
async def get_model_info():
    """Get information about loaded models and components"""
    
    try:
        info = {
            'nlp_engine': nlp_engine.get_model_info() if nlp_engine else None,
            'prediction_model': {
                'type': prediction_model.model_type,
                'is_trained': prediction_model.is_trained
            } if prediction_model else None,
            'components_status': {
                'document_processor': bool(document_processor),
                'nlp_engine': bool(nlp_engine),
                'prediction_model': bool(prediction_model),
                'skill_analyzer': bool(skill_analyzer),
                'upskilling_engine': bool(upskilling_engine),
                'feedback_generator': bool(feedback_generator),
                'role_matcher': bool(role_matcher)
            }
        }
        
        return info
        
    except Exception as e:
        logger.error(f"Error getting model info: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/feedback-only")
async def get_feedback_only(
    file: UploadFile = File(...),
    job_description: Optional[str] = Form(None),
    target_role: Optional[str] = Form(None)
):
    """Get detailed feedback and suggestions for resume improvement"""
    
    try:
        # Extract resume data
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp_file:
            shutil.copyfileobj(file.file, tmp_file)
            tmp_path = tmp_file.name
        
        extracted_data = document_processor.extract_structured_data(tmp_path)
        os.unlink(tmp_path)
        
        # Generate comprehensive feedback
        feedback_analysis = feedback_generator.analyze_resume(
            extracted_data.cleaned_text, job_description, target_role
        )
        
        # Format response
        results = {
            'overall_score': feedback_analysis.overall_score,
            'strengths': feedback_analysis.strengths,
            'weaknesses': feedback_analysis.weaknesses,
            'detailed_feedback': [
                {
                    'category': item.category,
                    'severity': item.severity,
                    'title': item.title,
                    'description': item.description,
                    'suggestion': item.suggestion,
                    'examples': item.examples,
                    'priority': item.priority
                }
                for item in feedback_analysis.feedback_items
            ],
            'keyword_optimization': feedback_analysis.keyword_optimization,
            'formatting_issues': feedback_analysis.formatting_issues,
            'content_suggestions': feedback_analysis.content_suggestions,
            'ats_compatibility': feedback_analysis.ats_compatibility,
            'improvement_report': feedback_generator.generate_improvement_report(feedback_analysis)
        }
        
        return AnalysisResponse(
            success=True,
            message="Feedback analysis completed successfully",
            data=results,
            processing_time=0.0
        )
        
    except Exception as e:
        logger.error(f"Error generating feedback: {e}")
        raise HTTPException(status_code=500, detail=f"Feedback generation failed: {str(e)}")

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "data": None,
            "processing_time": 0.0
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
            "data": None,
            "processing_time": 0.0
        }
    )

def get_company_job_matches(skills: List[str]) -> List[Dict[str, Any]]:
    """Get job matches with specific companies based on skills"""
    try:
        from company_jobs_data import COMPANY_JOBS
        company_jobs = COMPANY_JOBS
    except ImportError:
        # Fallback minimal job list
        company_jobs = [
            {
                'company': 'Google',
                'role_title': 'Software Engineer',
                'location': 'Bangalore, India',
                'salary_range': '₹25L - ₹45L',
                'experience_level': 'Mid-level',
                'job_type': 'Full-time',
                'required_skills': ['python', 'java', 'javascript', 'algorithms', 'data structures'],
                'preferred_skills': ['machine learning', 'cloud computing', 'kubernetes'],
                'company_size': '100,000+',
                'industry': 'Technology',
                'remote_friendly': True,
                'description': 'Build next-generation technologies.',
                'contact_info': {}
            }
        ]
    
    matches = []
    skills_lower = [skill.lower().strip() for skill in skills]
    
    for job in company_jobs:
        # Calculate skill matches
        required_matches = sum(1 for req_skill in job['required_skills'] 
                             if any(req_skill.lower() in skill_lower for skill_lower in skills_lower))
        preferred_matches = sum(1 for pref_skill in job['preferred_skills'] 
                              if any(pref_skill.lower() in skill_lower for skill_lower in skills_lower))
        
        total_required = len(job['required_skills'])
        total_preferred = len(job['preferred_skills'])
        
        if required_matches > 0:
            # Calculate fit score
            required_percentage = (required_matches / total_required) * 100
            preferred_percentage = (preferred_matches / total_preferred) * 100 if total_preferred > 0 else 0
            
            base_fit_score = (required_percentage * 0.8) + (preferred_percentage * 0.2)
            fit_score = min(98, int(base_fit_score))
            
            # Selection probability
            selection_probability = min(95, int(fit_score * 0.85 + (required_matches * 2)))
            
            # Get matching skills
            skills_overlap = [skill for skill in job['required_skills'] + job['preferred_skills']
                            if any(skill.lower() in skill_lower for skill_lower in skills_lower)]
            missing_skills = [skill for skill in job['required_skills']
                            if not any(skill.lower() in skill_lower for skill_lower in skills_lower)]
            
            matches.append({
                'company': job['company'],
                'role_title': job['role_title'],
                'location': job['location'],
                'salary_range': job['salary_range'],
                'experience_level': job['experience_level'],
                'job_type': job['job_type'],
                'company_size': job['company_size'],
                'industry': job['industry'],
                'remote_friendly': job['remote_friendly'],
                'description': job['description'],
                'contact_info': job.get('contact_info', {}),
                'fit_score': fit_score,
                'selection_probability': selection_probability,
                'skills_overlap': skills_overlap,
                'missing_skills': missing_skills,
                'required_skills_match': f"{required_matches}/{total_required}",
                'preferred_skills_match': f"{preferred_matches}/{total_preferred}"
            })
    
    # Sort by selection probability (interview success)
    matches.sort(key=lambda x: x['selection_probability'], reverse=True)
    return matches

@app.get("/api/v1/company-matches")
async def get_company_matches():
    """Get job matches with specific companies - requires resume to be uploaded first"""
    global uploaded_resume_data
    
    if not uploaded_resume_data:
        raise HTTPException(status_code=400, detail="No resume uploaded. Please upload a resume first.")
    
    skills = uploaded_resume_data.get('skills', [])
    if not skills:
        raise HTTPException(status_code=400, detail="No skills found in uploaded resume.")
    
    company_matches = get_company_job_matches(skills)
    
    return {
        "candidate_name": uploaded_resume_data.get('name', 'Unknown'),
        "total_skills": len(skills),
        "matches": company_matches,
        "total_matches": len(company_matches),
        "message": f"Found {len(company_matches)} company job matches"
    }

@app.post("/api/v1/store-resume")
async def store_resume_data(data: Dict[str, Any]):
    """Store resume data for later use (for company matches)"""
    global uploaded_resume_data
    uploaded_resume_data = data
    return {"success": True, "message": "Resume data stored"}

# Mount static files (for serving frontend if needed)
if Path("static").exists():
    app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=9002,
        reload=True,
        log_level="info"
    )
