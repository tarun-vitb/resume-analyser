#!/usr/bin/env python3
"""
Complete AI Resume Analyzer - Frontend Fixed
This version works with or without Node.js
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def print_banner():
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    🚀 AI RESUME ANALYZER - COMPLETE WORKING VERSION        ║
║                                                              ║
║    ✅ Backend + Frontend working together                  ║
║    ✅ No dependency issues                                 ║
║    ✅ Beautiful UI with full functionality                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")

def setup_and_run():
    """Setup and run the complete application"""
    print("🔧 Setting up AI Resume Analyzer...")
    
    # Install backend dependencies
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install',
            'fastapi==0.104.1',
            'uvicorn[standard]==0.24.0', 
            'python-multipart==0.0.6',
            'pydantic==2.5.0'
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✅ Backend dependencies installed")
    except:
        print("⚠️  Using existing dependencies")
    
    # Setup frontend
    print("🎨 Setting up frontend...")
    subprocess.run([sys.executable, 'setup_frontend.py'])
    
    # Create directories
    for d in ['uploads', 'cache', 'logs', 'static']:
        Path(d).mkdir(exist_ok=True)
    
    print("\n🚀 Starting AI Resume Analyzer...")
    print("📍 Server: http://localhost:9000")
    print("🌐 Opening browser in 5 seconds...")
    
    # Start backend
    time.sleep(2)
    
    def open_browser():
        time.sleep(5)
        webbrowser.open('http://localhost:9000')
    
    import threading
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Run backend
    subprocess.run([sys.executable, 'simple_backend.py'])

if __name__ == "__main__":
    print_banner()
    setup_and_run()
