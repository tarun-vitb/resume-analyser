@echo off
echo ======================================================================
echo Starting AI Resume Analyzer Frontend
echo ======================================================================

cd frontend-app

if not exist node_modules (
    echo.
    echo Installing dependencies...
    call npm install
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to install dependencies
        echo Make sure Node.js is installed: https://nodejs.org/
        pause
        exit /b 1
    )
)

echo.
echo Starting frontend server on port 5174...
echo Access at: http://localhost:5174
echo.
echo Press Ctrl+C to stop
echo.

call npm run dev

pause

