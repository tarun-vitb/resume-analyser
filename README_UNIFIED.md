# AI Resume Analyzer - Unified Application

This is a complete, production-ready AI Resume Analyzer & Job Recommendation Website with full frontend-backend integration.

## 🚀 Quick Start

### Option 1: Unified Startup (Recommended)

```bash
python start_unified_app.py
```

This will:
- Check all dependencies
- Install missing packages if needed
- Start the backend on port 9002
- Start the frontend on port 5174
- Open the browser automatically

### Option 2: Manual Startup

**Start Backend:**
```bash
python main.py
```
Backend runs on: http://localhost:9002

**Start Frontend:**
```bash
cd frontend-app
npm install  # First time only
npm run dev
```
Frontend runs on: http://localhost:5174

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

## 🔧 Installation

### Backend Dependencies
```bash
pip install -r requirements.txt
```

### Frontend Dependencies
```bash
cd frontend-app
npm install
```

### Additional Setup (Optional)

For full NLP capabilities, install spaCy model:
```bash
python -m spacy download en_core_web_sm
```

## 🌐 Access Points

Once running:

- **Frontend**: http://localhost:5174
- **Backend API**: http://localhost:9002
- **API Documentation**: http://localhost:9002/docs
- **Health Check**: http://localhost:9002/health

## ✨ Features

### 1. Resume Upload & Parsing
- ✅ Accepts PDF, DOCX, DOC files
- ✅ Validates file type and size (max 10MB)
- ✅ Extracts text using PyMuPDF and python-docx
- ✅ Handles errors gracefully

### 2. AI Resume Analysis
- ✅ Analyzes skills, experience, education, projects
- ✅ Compares resume with job requirements
- ✅ Generates resume strength score (fit_score)
- ✅ Calculates skill match percentage
- ✅ Lists missing skills
- ✅ Provides improvement suggestions

### 3. Job Role & Match Recommendations
- ✅ Predicts suitable job roles
- ✅ Recommends jobs from company database
- ✅ Shows probability/match score for each role
- ✅ Maps resume skills → job skill requirements

### 4. Frontend (UI/UX)
- ✅ Clean, modern, responsive UI
- ✅ Pages: Home, Analyze, Matches, About
- ✅ Displays resume score, skill match charts, missing skills
- ✅ AI suggestions and job recommendations
- ✅ Loading states, success/error messages
- ✅ Fully connected to backend APIs

### 5. Backend Integration
- ✅ REST API endpoints properly connected
- ✅ CORS enabled for frontend
- ✅ File handling and JSON responses
- ✅ Consistent endpoint naming

## 📡 API Endpoints

### Core Endpoints

#### `POST /api/v1/upload-resume`
Upload and extract text from resume file.

**Request:** Multipart form data with `file` field

**Response:**
```json
{
  "success": true,
  "message": "Resume uploaded and processed successfully",
  "name": "John Doe",
  "skills": ["Python", "JavaScript", "React"],
  "experience": [...],
  "education": [...]
}
```

#### `POST /api/v1/analyze-resume`
Comprehensive resume analysis against job description.

**Request:** Multipart form data with:
- `file`: Resume file
- `job_description`: Job description text
- `target_role`: (Optional) Target role
- `analysis_type`: (Optional) "basic", "comprehensive", or "detailed"

**Response:**
```json
{
  "success": true,
  "fit_score": 85,
  "shortlist_probability": 78,
  "skills": ["Python", "JavaScript"],
  "missing_skills": ["Docker", "Kubernetes"],
  "feedback": "Your resume shows good alignment...",
  "recommended_courses": [...],
  "eligible_jobs": [...]
}
```

#### `GET /api/v1/company-matches`
Get job matches with specific companies (requires resume upload first).

**Response:**
```json
{
  "candidate_name": "John Doe",
  "total_skills": 15,
  "matches": [
    {
      "company": "Google",
      "role_title": "Software Engineer",
      "fit_score": 88,
      "selection_probability": 82,
      "skills_overlap": [...],
      "missing_skills": [...]
    }
  ]
}
```

#### `GET /health`
Health check endpoint.

## 🏗️ Architecture

```
AI Resume Analyzer/
├── main.py                 # FastAPI backend (unified)
├── core/                   # Core AI/NLP modules
│   ├── document_processor.py
│   ├── nlp_engine.py
│   ├── skill_analyzer.py
│   ├── prediction_model.py
│   ├── role_matcher.py
│   ├── upskilling_engine.py
│   └── feedback_generator.py
├── frontend-app/           # React frontend
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   ├── Analyze.jsx
│   │   │   ├── Matches.jsx
│   │   │   └── About.jsx
│   │   ├── components/
│   │   └── config.js       # API configuration
│   └── package.json
├── company_jobs_data.py    # Company job database
├── requirements.txt        # Python dependencies
└── start_unified_app.py    # Unified startup script
```

## 🔍 How It Works

1. **User uploads resume** → Backend extracts text and skills
2. **User provides job description** → Backend analyzes match
3. **Analysis results** → Fit score, skill gaps, feedback
4. **Job recommendations** → Matched companies and roles
5. **Course suggestions** → Learning paths for missing skills

## 🐛 Troubleshooting

### Backend Issues

**Port 9002 already in use:**
```bash
# Windows
netstat -ano | findstr :9002
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:9002 | xargs kill -9
```

**Missing dependencies:**
```bash
pip install -r requirements.txt
```

**spaCy model not found:**
```bash
python -m spacy download en_core_web_sm
```

### Frontend Issues

**Port 5174 already in use:**
Change port in `frontend-app/package.json`:
```json
"dev": "vite --port 5174"
```

**Module not found:**
```bash
cd frontend-app
npm install
```

**CORS errors:**
Ensure backend CORS allows `http://localhost:5174`

## 📝 Notes

- The application uses in-memory storage for resume data (session-based)
- For production, consider adding a database for persistence
- Company job database can be expanded in `company_jobs_data.py`
- All AI models are loaded on startup (may take a few seconds)

## 🎯 Next Steps

- Add database persistence
- Implement user authentication
- Expand company job database
- Add more AI models/features
- Deploy to production

## 📄 License

This project is ready for portfolio/demo use.

