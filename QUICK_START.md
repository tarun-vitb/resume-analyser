# Quick Start Guide

## Option 1: Using Batch Files (Easiest for Windows)

### Start Backend:
Double-click `START_BACKEND.bat` or run:
```cmd
START_BACKEND.bat
```

### Start Frontend:
Double-click `START_FRONTEND.bat` or run:
```cmd
START_FRONTEND.bat
```

## Option 2: Using Command Line

### Terminal 1 - Backend:
```bash
python main.py
```

### Terminal 2 - Frontend:
```bash
cd frontend-app
npm install  # First time only
npm run dev
```

## Option 3: Using Python Scripts

### Backend:
```bash
python run_backend.py
```

### Frontend:
```bash
python run_frontend.py
```

## Access Points

- **Frontend**: http://localhost:5174
- **Backend API**: http://localhost:9002
- **API Documentation**: http://localhost:9002/docs

## First Time Setup

If you haven't installed dependencies yet:

### Backend Dependencies:
```bash
pip install -r requirements.txt
```

### Frontend Dependencies:
```bash
cd frontend-app
npm install
```

## Troubleshooting

### Port Already in Use

**Backend (port 9002):**
```cmd
netstat -ano | findstr :9002
taskkill /PID <PID_NUMBER> /F
```

**Frontend (port 5174):**
```cmd
netstat -ano | findstr :5174
taskkill /PID <PID_NUMBER> /F
```

### Missing Dependencies

**Python packages:**
```bash
pip install fastapi uvicorn python-multipart PyMuPDF python-docx sentence-transformers scikit-learn numpy pandas pydantic
```

**Node packages:**
```bash
cd frontend-app
npm install
```

### Node.js Not Found

Install Node.js from: https://nodejs.org/

## Common Issues

1. **"ModuleNotFoundError"** → Install Python dependencies
2. **"npm is not recognized"** → Install Node.js
3. **"Port already in use"** → Kill process or change port
4. **"Cannot connect"** → Make sure backend is running first

For more details, see `TROUBLESHOOTING.md`

