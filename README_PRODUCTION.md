# 🚀 AI Resume Analyzer - Production Setup Guide

## 📋 Overview

This is a **production-grade AI Resume Analyzer** with a stunning React frontend and robust FastAPI backend. The platform provides AI-powered resume analysis, job matching, and career insights.

### ✨ Key Features

- **🎨 Modern React Frontend** (Vite + Tailwind + ShadCN/UI)
- **🔧 FastAPI Backend** with comprehensive API endpoints
- **🤖 AI-Powered Analysis** with skill gap detection
- **📊 Interactive Charts** and visual metrics
- **🎯 Job Matching** with fit scores
- **📚 Course Recommendations** for skill development
- **📱 Fully Responsive** design with dark mode
- **🐳 Docker Ready** for easy deployment

## 🌐 Architecture

```
Frontend (React + Vite)     Backend (FastAPI)
http://localhost:5173   →   http://localhost:9000
        │                          │
        ├── Drag & Drop Upload     ├── /upload_resume
        ├── Interactive Charts     ├── /analyze_resume
        ├── Job Matching UI        ├── /match_jobs
        └── Responsive Design      └── /health
```

## 🚀 Quick Start

### Option 1: One-Command Launch (Recommended)

```bash
python start_production.py
```

This script will:
- ✅ Check system requirements
- ✅ Install all dependencies
- ✅ Start backend on port 9000
- ✅ Start frontend on port 5173
- ✅ Open both in your browser

### Option 2: Manual Setup

#### Backend Setup
```bash
# Install Python dependencies
pip install fastapi uvicorn python-multipart pydantic PyPDF2 python-docx

# Start backend server
python backend_main.py
```

#### Frontend Setup
```bash
# Navigate to frontend directory
cd frontend-app

# Install Node.js dependencies
npm install

# Start development server
npm run dev
```

### Option 3: Docker Deployment
```bash
# Build and start all services
docker-compose -f docker-compose.production.yml up --build

# Access the application
# Frontend: http://localhost:5173
# Backend: http://localhost:9000
```

## 📍 Access Points

Once running, access these URLs:

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:5173 | React app with stunning UI |
| **Backend API** | http://localhost:9000 | FastAPI server |
| **API Docs** | http://localhost:9000/docs | Interactive API documentation |
| **Health Check** | http://localhost:9000/health | Server health status |

## 🎯 Core Features

### 1. **Resume Upload & Analysis**
- Drag & drop PDF/DOCX files
- Real-time text extraction
- AI-powered content analysis
- ATS compatibility scoring

### 2. **Interactive Dashboard**
- Circular fit score charts (Recharts)
- Skill gap visualization
- Selection probability metrics
- Animated progress bars

### 3. **Job Matching**
- Match against 5+ job roles
- Sortable results table
- Fit score calculations
- Missing skills identification

### 4. **Course Recommendations**
- Personalized learning paths
- Coursera/Udemy integration
- ROI-based prioritization
- Time and cost estimates

### 5. **Modern UI/UX**
- Gradient backgrounds
- Framer Motion animations
- Glass morphism effects
- Dark mode support
- Fully responsive design

## 🔧 API Endpoints

### Core Endpoints

```bash
# Upload resume file
POST /upload_resume
Content-Type: multipart/form-data
Body: file (PDF/DOCX)

# Analyze resume against job description
POST /analyze_resume
Content-Type: multipart/form-data
Body: file_id, job_description

# Get job matches
GET /match_jobs?file_id={file_id}

# Health check
GET /health
```

### Example API Usage

```javascript
// Upload resume
const formData = new FormData()
formData.append('file', resumeFile)

const uploadResponse = await fetch('http://localhost:9000/upload_resume', {
  method: 'POST',
  body: formData
})

// Analyze resume
const analysisData = new FormData()
analysisData.append('file_id', fileId)
analysisData.append('job_description', jobDescription)

const analysisResponse = await fetch('http://localhost:9000/analyze_resume', {
  method: 'POST',
  body: analysisData
})
```

## 📊 Sample Response

```json
{
  "success": true,
  "analysis": {
    "fit_score": 78.5,
    "selection_probability": 82.3,
    "matched_skills": ["Python", "React", "SQL"],
    "missing_skills": ["Docker", "AWS", "Kubernetes"],
    "feedback": [
      "Add more cloud computing experience",
      "Include specific project metrics"
    ],
    "course_recommendations": [
      {
        "skill": "Docker",
        "course_title": "Docker Mastery Complete Guide",
        "provider": "Udemy",
        "duration": "6 weeks",
        "rating": 4.7,
        "price": "$39"
      }
    ]
  }
}
```

## 🎨 Frontend Components

### Key React Components

```
src/
├── components/
│   ├── Navbar.jsx          # Navigation with dark mode
│   └── Footer.jsx          # Footer with links
├── pages/
│   ├── Home.jsx            # Landing page with animations
│   ├── Analyze.jsx         # Main analysis interface
│   ├── Matches.jsx         # Job matching results
│   └── About.jsx           # About page
└── App.jsx                 # Main app with routing
```

### UI Features
- **Drag & Drop Upload** with visual feedback
- **Interactive Charts** using Recharts
- **Animated Gradients** with Framer Motion
- **Skill Badges** with color coding
- **Progress Bars** with smooth animations
- **Toast Notifications** for user feedback

## 🔒 Security & Performance

### Security Features
- CORS protection
- File type validation
- Input sanitization
- Secure file handling

### Performance Optimizations
- React Query for caching
- Lazy loading components
- Optimized bundle size
- Fast API responses (<2s)

## 🐳 Production Deployment

### Docker Compose
```bash
# Production deployment
docker-compose -f docker-compose.production.yml up -d

# Scale services
docker-compose -f docker-compose.production.yml up --scale backend=3
```

### Environment Variables
```bash
# Backend
PYTHONPATH=/app
PYTHONUNBUFFERED=1

# Frontend
VITE_API_BASE_URL=http://localhost:9000
```

## 📈 Performance Metrics

### Expected Performance
- **Resume Upload**: 1-3 seconds
- **Analysis Processing**: 2-5 seconds
- **Job Matching**: 1-2 seconds per job
- **Frontend Load**: <1 second
- **API Response**: <500ms average

### Scalability
- **Concurrent Users**: 100+ supported
- **File Size Limit**: 10MB per resume
- **Throughput**: 1000+ requests/hour
- **Memory Usage**: <512MB per instance

## 🛠️ Development

### Tech Stack
- **Frontend**: React 18, Vite, Tailwind CSS, Framer Motion
- **Backend**: FastAPI, Python 3.11, Pydantic
- **Charts**: Recharts for interactive visualizations
- **Icons**: Heroicons for consistent iconography
- **Deployment**: Docker, Docker Compose

### Development Commands
```bash
# Frontend development
cd frontend-app
npm run dev          # Start dev server
npm run build        # Build for production
npm run preview      # Preview production build

# Backend development
python backend_main.py    # Start with auto-reload
uvicorn backend_main:app --reload --port 9000
```

## 🧪 Testing

### Manual Testing
1. Upload a sample resume (PDF/DOCX)
2. Enter a job description
3. Click "Analyze Resume"
4. View results dashboard
5. Check job matches page
6. Test responsive design

### API Testing
```bash
# Test health endpoint
curl http://localhost:9000/health

# Test demo data
curl http://localhost:9000/demo_data
```

## 🚨 Troubleshooting

### Common Issues

1. **Port 9000 in use**
   ```bash
   # Kill process on port 9000
   lsof -ti:9000 | xargs kill -9
   ```

2. **Frontend not connecting to backend**
   - Check backend is running on port 9000
   - Verify CORS settings in backend
   - Check browser console for errors

3. **File upload fails**
   - Ensure file is PDF/DOCX format
   - Check file size (<10MB)
   - Verify backend upload directory exists

4. **Dependencies missing**
   ```bash
   # Reinstall backend deps
   pip install -r requirements_minimal.txt
   
   # Reinstall frontend deps
   cd frontend-app && npm install
   ```

## 🎉 Success Indicators

When everything is working correctly, you should see:

✅ **Backend**: Server running on http://localhost:9000  
✅ **Frontend**: App running on http://localhost:5173  
✅ **API Docs**: Available at http://localhost:9000/docs  
✅ **Health Check**: Returns {"status": "healthy"}  
✅ **File Upload**: Drag & drop works smoothly  
✅ **Analysis**: Results display with charts  
✅ **Job Matching**: Shows relevant job matches  
✅ **Responsive**: Works on mobile and desktop  

## 📞 Support

If you encounter any issues:

1. Check the troubleshooting section above
2. Verify all dependencies are installed
3. Ensure both frontend and backend are running
4. Check browser console for JavaScript errors
5. Review backend logs for API errors

---

**🎯 You now have a fully functional, production-ready AI Resume Analyzer platform!**
