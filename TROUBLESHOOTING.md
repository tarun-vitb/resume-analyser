# Troubleshooting Guide

## Common Issues and Solutions

### Backend Won't Start

#### 1. **Port Already in Use**
**Error:** `Address already in use` or `Port 9002 is already in use`

**Solution:**
```bash
# Windows - Find and kill process on port 9002
netstat -ano | findstr :9002
taskkill /PID <PID_NUMBER> /F

# Or change port in main.py (line ~760)
# Change: port=9002 to port=9003 (or any free port)
```

#### 2. **Missing Dependencies**
**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```bash
pip install -r requirements.txt
```

If that fails, install individually:
```bash
pip install fastapi uvicorn python-multipart PyMuPDF python-docx sentence-transformers scikit-learn numpy pandas pydantic
```

#### 3. **Syntax Error in main.py**
**Error:** `SyntaxError: invalid syntax`

**Solution:**
- Check if the file was corrupted
- Try: `python -m py_compile main.py` to find syntax errors
- Restore from git if needed

#### 4. **Import Errors from Core Modules**
**Error:** `ModuleNotFoundError: No module named 'core.document_processor'`

**Solution:**
- Make sure you're running from the project root directory
- Check that `core/` directory exists
- Verify `core/__init__.py` exists

#### 5. **spaCy Model Missing**
**Error:** `OSError: Can't find model 'en_core_web_sm'`

**Solution:**
```bash
python -m spacy download en_core_web_sm
```

#### 6. **Memory Errors During Startup**
**Error:** `MemoryError` or slow startup

**Solution:**
- Models are large. First startup may take time.
- If it fails, you may need more RAM or reduce model size in `core/nlp_engine.py`

### Frontend Won't Start

#### 1. **Port Already in Use**
**Error:** `Port 5174 is already in use`

**Solution:**
```bash
# Windows
netstat -ano | findstr :5174
taskkill /PID <PID_NUMBER> /F

# Or change port in frontend-app/package.json
# Change: "dev": "vite --port 5174" to "dev": "vite --port 5175"
```

#### 2. **node_modules Missing**
**Error:** `Cannot find module` errors

**Solution:**
```bash
cd frontend-app
npm install
```

#### 3. **Node.js Not Found**
**Error:** `'npm' is not recognized as an internal or external command`

**Solution:**
- Install Node.js from https://nodejs.org/
- Restart terminal after installation
- Verify: `node --version` and `npm --version`

#### 4. **Package Installation Errors**
**Error:** `npm ERR!` messages

**Solution:**
```bash
cd frontend-app
rm -rf node_modules package-lock.json  # Linux/Mac
# OR
rmdir /s node_modules  # Windows
del package-lock.json

npm install
```

### Connection Issues

#### 1. **CORS Errors in Browser**
**Error:** `Access to XMLHttpRequest blocked by CORS policy`

**Solution:**
- Backend CORS is configured in `main.py` (line ~76-82)
- Make sure frontend URL is in `allow_origins` list
- Backend should allow `http://localhost:5174`

#### 2. **API Endpoints Not Found**
**Error:** `404 Not Found` when calling API

**Solution:**
- Check backend is running on port 9002
- Verify endpoint URLs in `frontend-app/src/config.js`
- Check backend logs for actual endpoints

#### 3. **Connection Refused**
**Error:** `ERR_CONNECTION_REFUSED`

**Solution:**
- Make sure backend is running
- Check backend is on correct port (9002)
- Verify firewall isn't blocking the connection

## Step-by-Step Debugging

### 1. Test Backend Alone

```bash
python main.py
```

Should see:
```
INFO:     Uvicorn running on http://0.0.0.0:9002
INFO:     Application startup complete.
```

Then test in browser: http://localhost:9002/health

### 2. Test Frontend Alone

```bash
cd frontend-app
npm run dev
```

Should see:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5174/
```

### 3. Check API Connection

Open browser console (F12) and check for errors when frontend loads.

### 4. Verify Dependencies

**Python:**
```bash
python -c "import fastapi, uvicorn; print('OK')"
```

**Node:**
```bash
cd frontend-app
npm list --depth=0
```

## Quick Fix Scripts

### Run with Error Handling

**Backend:**
```bash
python run_backend.py
```

**Frontend:**
```bash
python run_frontend.py
```

These scripts will:
- Check dependencies
- Provide clear error messages
- Guide you to solutions

## Still Having Issues?

1. **Check the error message** - It usually tells you what's wrong
2. **Check logs** - Both backend and frontend show error details
3. **Verify file structure** - Make sure all files are in correct locations
4. **Check Python/Node versions** - Python 3.8+, Node 16+

## Getting Help

When asking for help, provide:
1. Exact error message
2. What command you ran
3. Python version: `python --version`
4. Node version: `node --version`
5. Operating system

