#!/usr/bin/env python3
"""
Quick Start Script - Fixed for Windows
No complex dependencies, works out of the box
"""

import os
import sys
import subprocess
import platform
import time
import threading
import webbrowser
from pathlib import Path

def print_banner():
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    🚀 AI RESUME ANALYZER - QUICK START (FIXED)             ║
║                                                              ║
║    Simple version that works on Windows without issues      ║
║    Backend:  http://localhost:9000                          ║
║    Frontend: http://localhost:5173                          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)

def install_simple_deps():
    """Install only essential dependencies"""
    print("📦 Installing simple dependencies...")
    
    try:
        deps = [
            'fastapi==0.104.1',
            'uvicorn[standard]==0.24.0', 
            'python-multipart==0.0.6',
            'pydantic==2.5.0'
        ]
        
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install'
        ] + deps, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        print("✅ Backend dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def install_frontend():
    """Install frontend dependencies"""
    print("📦 Installing frontend dependencies...")
    
    frontend_dir = Path('frontend-app')
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    try:
        os.chdir(frontend_dir)
        subprocess.check_call(['npm', 'install'], 
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✅ Frontend dependencies installed")
        os.chdir('..')
        return True
    except subprocess.CalledProcessError:
        print("❌ Frontend setup failed")
        os.chdir('..')
        return False
    except FileNotFoundError:
        print("❌ Node.js/npm not found")
        os.chdir('..')
        return False

def create_dirs():
    """Create necessary directories"""
    dirs = ['uploads', 'cache', 'logs']
    for d in dirs:
        Path(d).mkdir(exist_ok=True)
    print("✅ Directories created")

def start_backend():
    """Start the simple backend"""
    print("🔧 Starting backend...")
    try:
        subprocess.run([sys.executable, 'simple_backend.py'])
    except KeyboardInterrupt:
        print("🛑 Backend stopped")

def start_frontend():
    """Start React frontend"""
    print("🎨 Starting frontend...")
    frontend_dir = Path('frontend-app')
    
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return
    
    try:
        os.chdir(frontend_dir)
        subprocess.run(['npm', 'run', 'dev'])
    except KeyboardInterrupt:
        print("🛑 Frontend stopped")
    except Exception as e:
        print(f"❌ Frontend error: {e}")
    finally:
        os.chdir('..')

def test_backend():
    """Test backend health"""
    print("🧪 Testing backend...")
    time.sleep(3)
    
    try:
        import urllib.request
        response = urllib.request.urlopen('http://localhost:9000/health', timeout=10)
        if response.getcode() == 200:
            print("✅ Backend is healthy")
            return True
        else:
            print(f"⚠️  Backend responded with {response.getcode()}")
            return False
    except Exception as e:
        print(f"❌ Backend test failed: {e}")
        return False

def open_browser():
    """Open browser after delay"""
    time.sleep(8)
    try:
        webbrowser.open('http://localhost:5173')
        print("🌐 Opened browser")
    except:
        pass

def main():
    """Main function"""
    print_banner()
    
    print("🔍 Checking Python...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required. Current: {version.major}.{version.minor}")
        input("Press Enter to exit...")
        return
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    
    # Setup
    print("\n🚀 Setting up application...")
    create_dirs()
    
    if not install_simple_deps():
        print("⚠️  Backend setup failed, but continuing...")
    
    if not install_frontend():
        print("⚠️  Frontend setup failed, but continuing...")
    
    print("\n" + "="*60)
    print("🎯 READY TO LAUNCH!")
    print("="*60)
    print("📍 Backend will start on: http://localhost:9000")
    print("📍 Frontend will start on: http://localhost:5173")
    print("📚 API Documentation: http://localhost:9000/docs")
    print("💚 Health Check: http://localhost:9000/health")
    print()
    print("🎨 FEATURES:")
    print("   • Upload resume files (PDF/DOCX/TXT)")
    print("   • AI-powered analysis and scoring")
    print("   • Job matching with fit scores")
    print("   • Skill gap detection")
    print("   • Course recommendations")
    print("   • Interactive charts and visualizations")
    print("="*60)
    
    # Start application
    print("\n🚀 Starting backend server...")
    
    # Start backend in thread
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    # Test backend
    if test_backend():
        print("✅ Backend ready!")
    
    # Open browser in background
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    print("🎨 Starting frontend server...")
    print("🌐 Browser will open automatically")
    print("\nPress Ctrl+C to stop both servers")
    print("-" * 60)
    
    # Start frontend (blocking)
    try:
        start_frontend()
    except KeyboardInterrupt:
        print("\n👋 Application stopped")

if __name__ == "__main__":
    main()
