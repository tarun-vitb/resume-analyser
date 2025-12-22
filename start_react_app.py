"""
Complete AI Resume Analyzer Startup Script
Starts both the fixed backend and React frontend
"""

import subprocess
import sys
import time
import webbrowser
from pathlib import Path
import threading
import os

def install_python_requirements():
    """Install Python backend requirements"""
    print("Installing Python backend requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn", "python-multipart", "requests"], 
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✓ Python packages installed!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing Python packages: {e}")
        return False

def install_node_dependencies():
    """Install Node.js frontend dependencies"""
    frontend_path = Path("frontend-app")
    if not frontend_path.exists():
        print("✗ Frontend directory not found!")
        return False
    
    print("Installing Node.js frontend dependencies...")
    try:
        # Check if node_modules exists
        if not (frontend_path / "node_modules").exists():
            subprocess.check_call(["npm", "install"], cwd=frontend_path, 
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✓ Node.js packages ready!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing Node.js packages: {e}")
        print("   Make sure Node.js and npm are installed")
        return False
    except FileNotFoundError:
        print("✗ npm not found. Please install Node.js and npm")
        return False

def start_backend():
    """Start the backend server"""
    print("🔥 Starting backend server on port 9002...")
    try:
        subprocess.run([sys.executable, "fixed_enhanced_backend.py"])
    except KeyboardInterrupt:
        print("Backend stopped")
    except Exception as e:
        print(f"Backend error: {e}")

def start_frontend():
    """Start the React frontend"""
    frontend_path = Path("frontend-app")
    print("🚀 Starting React frontend on port 5173...")
    try:
        subprocess.run(["npm", "run", "dev"], cwd=frontend_path)
    except KeyboardInterrupt:
        print("Frontend stopped")
    except Exception as e:
        print(f"Frontend error: {e}")

def open_browser_delayed():
    """Open browser after services start"""
    time.sleep(8)  # Wait for both services to start
    print("🌐 Opening browser...")
    webbrowser.open("http://localhost:5173")

def main():
    """Main function"""
    print("="*70)
    print("🤖 AI RESUME ANALYZER - COMPLETE APPLICATION STARTUP")
    print("="*70)
    print("🎯 Starting both backend and React frontend...")
    print("   • Backend (Python FastAPI): http://localhost:9002")
    print("   • Frontend (React): http://localhost:5173")
    print("   • Fixed API connection and skill extraction")
    
    # Check required files
    if not Path("fixed_enhanced_backend.py").exists():
        print("✗ Backend file not found!")
        return
    
    if not Path("frontend-app").exists():
        print("✗ Frontend directory not found!")
        return
    
    # Install dependencies
    print("\n📦 Installing dependencies...")
    if not install_python_requirements():
        return
    
    if not install_node_dependencies():
        return
    
    print("\n🚀 Starting services...")
    
    # Start browser opener in background
    browser_thread = threading.Thread(target=open_browser_delayed)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Start backend in background
    backend_thread = threading.Thread(target=start_backend)
    backend_thread.daemon = True
    backend_thread.start()
    
    print("✓ Backend started on http://localhost:9002")
    
    # Wait a moment for backend to start
    time.sleep(3)
    
    # Start frontend (this will block)
    print("✓ Starting frontend on http://localhost:5173")
    try:
        start_frontend()
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")

if __name__ == "__main__":
    main()
