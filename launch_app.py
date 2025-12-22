#!/usr/bin/env python3
"""
🚀 AI Resume Analyzer - Complete Launch Script
Production-ready startup for both backend and frontend
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
║    🚀 AI RESUME ANALYZER - PRODUCTION LAUNCH v2.0          ║
║                                                              ║
║    Professional SaaS-Grade Resume Analysis Platform         ║
║    Frontend: http://localhost:5173                          ║
║    Backend:  http://localhost:9000                          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)

def check_system():
    """Check system requirements"""
    print("🔍 Checking system requirements...")
    
    # Check Python
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required. Current: {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    
    # Check Node.js
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✅ Node.js {result.stdout.strip()}")
        else:
            print("❌ Node.js not found")
            return False
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print("❌ Node.js not found or not responding")
        return False
    
    return True

def install_backend():
    """Install backend dependencies"""
    print("\n📦 Setting up backend...")
    
    try:
        # Install core dependencies
        deps = [
            'fastapi==0.104.1',
            'uvicorn[standard]==0.24.0',
            'python-multipart==0.0.6',
            'pydantic==2.5.0',
            'PyPDF2==3.0.1',
            'python-docx==0.8.11',
            'requests==2.31.0'
        ]
        
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + deps, 
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✅ Backend dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Backend setup failed")
        return False

def install_frontend():
    """Install frontend dependencies"""
    print("📦 Setting up frontend...")
    
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

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    dirs = ['uploads', 'cache', 'logs']
    for d in dirs:
        Path(d).mkdir(exist_ok=True)
    print("✅ Directories created")

def start_backend():
    """Start FastAPI backend"""
    print("🔧 Starting backend server...")
    try:
        subprocess.run([sys.executable, 'backend_main.py'])
    except KeyboardInterrupt:
        print("🛑 Backend stopped")
    except Exception as e:
        print(f"❌ Backend error: {e}")

def start_frontend():
    """Start React frontend"""
    print("🎨 Starting frontend server...")
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
        import requests
        response = requests.get('http://localhost:9000/health', timeout=10)
        if response.status_code == 200:
            print("✅ Backend is healthy")
            return True
        else:
            print(f"⚠️  Backend responded with {response.status_code}")
            return False
    except ImportError:
        print("⚠️  Requests not available, skipping test")
        return True
    except Exception as e:
        print(f"❌ Backend test failed: {e}")
        return False

def open_browser():
    """Open browser to the application"""
    time.sleep(8)  # Wait for servers to start
    try:
        webbrowser.open('http://localhost:5173')
        print("🌐 Opened browser to http://localhost:5173")
    except Exception as e:
        print(f"⚠️  Could not open browser: {e}")

def show_info():
    """Show application information"""
    print("\n" + "="*60)
    print("🎯 AI RESUME ANALYZER - READY!")
    print("="*60)
    print()
    print("🌐 ACCESS POINTS:")
    print("   • Frontend:     http://localhost:5173")
    print("   • Backend API:  http://localhost:9000")
    print("   • API Docs:     http://localhost:9000/docs")
    print("   • Health Check: http://localhost:9000/health")
    print()
    print("🎨 FEATURES:")
    print("   • Drag & drop resume upload (PDF/DOCX)")
    print("   • AI-powered analysis with charts")
    print("   • Job matching with fit scores")
    print("   • Skill gap detection")
    print("   • Course recommendations")
    print("   • Responsive design with animations")
    print()
    print("🔧 TECH STACK:")
    print("   • Backend:  FastAPI + Python")
    print("   • Frontend: React + Vite + Tailwind")
    print("   • Charts:   Recharts")
    print("   • Icons:    Heroicons")
    print("   • Animations: Framer Motion")
    print()
    print("📋 USAGE:")
    print("   1. Upload your resume (PDF/DOCX)")
    print("   2. Enter job description")
    print("   3. Click 'Analyze Resume'")
    print("   4. View results and recommendations")
    print("   5. Check job matches")
    print()
    print("="*60)

def main():
    """Main execution"""
    print_banner()
    
    # System checks
    if not check_system():
        input("Press Enter to exit...")
        return
    
    # Setup
    print("\n🚀 Setting up AI Resume Analyzer...")
    
    success = True
    if not install_backend():
        success = False
    if not install_frontend():
        success = False
    
    create_directories()
    
    if not success:
        print("\n⚠️  Some setup steps failed, but continuing...")
    
    show_info()
    
    # Start application
    print("\n🚀 Starting application...")
    print("⏳ Backend starting on port 9000...")
    
    # Start backend in thread
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    # Test backend
    if test_backend():
        print("✅ Backend ready!")
    
    # Open browser in background
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    print("⏳ Frontend starting on port 5173...")
    print("\n🌐 Application will open in your browser automatically")
    print("📍 Manual access: http://localhost:5173")
    print("\nPress Ctrl+C to stop both servers")
    print("-" * 60)
    
    # Start frontend (blocking)
    try:
        start_frontend()
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
