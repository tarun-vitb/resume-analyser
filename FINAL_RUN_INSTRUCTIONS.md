# 🚀 AI Resume Analyzer - Complete Setup & Run Instructions

## 📋 Overview
This is a complete, fully functional AI Resume Analyzer with:
- **FastAPI Backend** with real NLP analysis using Sentence-BERT
- **React Frontend** with Tailwind CSS and modern UI components
- **Real-time analysis** with semantic similarity and skill matching
- **Course recommendations** and job role suggestions

## 🛠️ Prerequisites
- Python 3.8+ installed
- Node.js 16+ and npm installed
- Git (optional)

## 🚀 Quick Start

### 1. Backend Setup & Run

```bash
# Navigate to the project directory
cd "c:\Users\prana\Downloads\AI-Resume-Analyzer-1\AI Resume Analyzer"

# Install Python dependencies
pip install -r requirements_final.txt

# Run the FastAPI backend
python backend_final.py
```

**Backend will be available at:** `http://localhost:9001`

### 2. Frontend Setup & Run

Open a **new terminal/command prompt** and run:

```bash
# Navigate to frontend directory
cd "c:\Users\prana\Downloads\AI-Resume-Analyzer-1\AI Resume Analyzer\frontend-app"

# Install dependencies (first time only)
npm install

# Run the React frontend
npm run dev
```

**Frontend will be available at:** `http://localhost:5174`

## 🎯 How to Use

1. **Open your browser** and go to `http://localhost:5174`
2. **Upload a resume** (PDF or DOCX format)
3. **Enter a job description** in the text area
4. **Click "Analyze Resume"** to get instant AI-powered analysis
5. **View results** including:
   - Fit Score (0-100%)
   - Shortlisting Probability
   - Skills Analysis (Present vs Missing)
   - AI Feedback
   - Course Recommendations
   - Eligible Job Roles

## 🔧 Technical Features

### Backend (`backend_final.py`)
- **Real NLP Analysis** using Sentence-BERT (all-MiniLM-L6-v2)
- **Document Processing** for PDF and DOCX files
- **Skill Extraction** with comprehensive keyword matching
- **Semantic Similarity** calculation between resume and job description
- **Dynamic Scoring** - no hardcoded values or zeros
- **CORS enabled** for frontend connection

### Frontend (React + Tailwind)
- **Modern UI** with gradient backgrounds and animations
- **Drag & Drop** file upload with visual feedback
- **Real-time Charts** using Recharts library
- **Responsive Design** works on all screen sizes
- **Loading States** and error handling
- **Professional Styling** with Tailwind CSS

## 📊 API Endpoints

### POST `/upload_resume`
- Accepts PDF/DOCX files
- Extracts text and basic information
- Returns candidate name and skills

### POST `/analyze`
- Accepts job description
- Performs NLP analysis
- Returns complete analysis results

### GET `/health`
- Health check endpoint

## 🎨 UI Components

- **File Upload Area** with drag & drop support
- **Job Description Input** with character counter
- **Circular Progress Chart** for fit score
- **Bar Charts** for skills analysis
- **Skill Tags** for present and missing skills
- **Course Cards** with external links
- **Job Role Cards** with match percentages

## 🔍 Analysis Features

### Real NLP Processing
- **Sentence-BERT Embeddings** for semantic similarity
- **Cosine Similarity** calculation
- **Dynamic Skill Extraction** from both resume and job description
- **Intelligent Scoring** combining multiple factors

### Comprehensive Results
- **Fit Score**: 0-100% based on semantic similarity and skill match
- **Shortlist Probability**: Realistic percentage based on analysis
- **Skills Analysis**: Present skills vs missing skills
- **Personalized Feedback**: AI-generated improvement suggestions
- **Course Recommendations**: Relevant courses for missing skills
- **Job Suggestions**: Eligible roles based on current skills

## 🚨 Troubleshooting

### Backend Issues
- **Port 9001 in use**: Change port in `backend_final.py` line 347
- **Module not found**: Run `pip install -r requirements_final.txt`
- **CORS errors**: Backend includes CORS middleware for localhost:5174

### Frontend Issues
- **Port 5174 in use**: Change port in `package.json` dev script
- **Dependencies missing**: Run `npm install` in frontend-app directory
- **API connection failed**: Ensure backend is running on port 9001

### Common Solutions
- **Restart both servers** if you encounter connection issues
- **Check firewall settings** if localhost access is blocked
- **Use different ports** if default ports are occupied

## 📁 File Structure

```
AI Resume Analyzer/
├── backend_final.py          # Main FastAPI backend
├── requirements_final.txt    # Python dependencies
├── frontend-app/            # React frontend
│   ├── src/
│   │   ├── pages/Analyze.jsx # Main analysis page
│   │   ├── config.js        # API configuration
│   │   └── ...
│   ├── package.json         # Node dependencies
│   └── ...
└── FINAL_RUN_INSTRUCTIONS.md # This file
```

## ✅ Verification Steps

1. **Backend Health Check**: Visit `http://localhost:9001/health`
2. **Frontend Loading**: Visit `http://localhost:5174`
3. **File Upload Test**: Upload a sample PDF/DOCX resume
4. **Analysis Test**: Enter job description and click analyze
5. **Results Display**: Verify all sections show real data (no zeros)

## 🎉 Success Indicators

- ✅ Backend shows "Models loaded successfully!" message
- ✅ Frontend loads without console errors
- ✅ File upload shows extracted skills and candidate name
- ✅ Analysis returns realistic scores (not 0% or 100%)
- ✅ All result sections display properly
- ✅ Course links are clickable and functional

## 📞 Support

If you encounter any issues:
1. Check that both servers are running
2. Verify the ports (9001 for backend, 5174 for frontend)
3. Ensure all dependencies are installed
4. Check browser console for error messages

**The application is now ready for full functionality testing!**
