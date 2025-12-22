#!/usr/bin/env python3
"""
Production-Grade AI Resume Analyzer Startup Script
Starts both backend (port 9000) and frontend (port 5173)
"""

import os
import sys
import subprocess
import platform
import time
import threading
from pathlib import Path

def print_banner():
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║        🚀 AI Resume Analyzer - Production Launch           ║
║                                                              ║
║     Professional SaaS-Grade Resume Analysis Platform        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking system requirements...")
    
    # Check Python version
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required. Current: {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    
    # Check Node.js
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js {result.stdout.strip()}")
        else:
            print("❌ Node.js not found. Please install Node.js 18+")
            return False
    except FileNotFoundError:
        print("❌ Node.js not found. Please install Node.js 18+")
        return False
    
    # Check npm
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ npm {result.stdout.strip()}")
        else:
            print("❌ npm not found")
            return False
    except FileNotFoundError:
        print("❌ npm not found")
        return False
    
    return True

def install_backend_deps():
    """Install backend dependencies"""
    print("\n📦 Installing backend dependencies...")
    
    backend_deps = [
        'fastapi==0.104.1',
        'uvicorn[standard]==0.24.0',
        'python-multipart==0.0.6',
        'pydantic==2.5.0',
        'PyPDF2==3.0.1',
        'python-docx==0.8.11'
    ]
    
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install'
        ] + backend_deps)
        print("✅ Backend dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install backend dependencies: {e}")
        return False

def install_frontend_deps():
    """Install frontend dependencies"""
    print("\n📦 Installing frontend dependencies...")
    
    frontend_dir = Path('frontend-app')
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    try:
        os.chdir(frontend_dir)
        subprocess.check_call(['npm', 'install'])
        print("✅ Frontend dependencies installed")
        os.chdir('..')
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install frontend dependencies: {e}")
        os.chdir('..')
        return False

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = ['uploads', 'cache', 'logs']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ {directory}/")

def start_backend():
    """Start the FastAPI backend"""
    print("\n🔧 Starting FastAPI backend on port 9000...")
    
    try:
        subprocess.run([
            sys.executable, 'backend_main.py'
        ])
    except KeyboardInterrupt:
        print("\n🛑 Backend stopped")
    except Exception as e:
        print(f"❌ Backend error: {e}")

def start_frontend():
    """Start the React frontend"""
    print("\n🎨 Starting React frontend on port 5173...")
    
    frontend_dir = Path('frontend-app')
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return
    
    try:
        os.chdir(frontend_dir)
        subprocess.run(['npm', 'run', 'dev'])
    except KeyboardInterrupt:
        print("\n🛑 Frontend stopped")
    except Exception as e:
        print(f"❌ Frontend error: {e}")
    finally:
        os.chdir('..')

def test_backend():
    """Test if backend is running"""
    print("\n🧪 Testing backend connection...")
    
    import time
    time.sleep(3)  # Wait for backend to start
    
    try:
        import requests
        response = requests.get('http://localhost:9000/health', timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running and healthy")
            return True
        else:
            print(f"⚠️  Backend responded with status {response.status_code}")
            return False
    except ImportError:
        print("⚠️  requests not installed, skipping backend test")
        return True
    except Exception as e:
        print(f"❌ Backend test failed: {e}")
        return False

def show_access_info():
    """Show access information"""
    print("\n" + "="*60)
    print("🌐 AI RESUME ANALYZER - ACCESS INFORMATION")
    print("="*60)
    print()
    print("🎨 FRONTEND (React + Vite):")
    print("   • URL: http://localhost:5173")
    print("   • Features: Drag & drop, animations, charts")
    print("   • UI: ShadCN/UI + Tailwind CSS")
    print()
    print("🔧 BACKEND (FastAPI):")
    print("   • URL: http://localhost:9000")
    print("   • API Docs: http://localhost:9000/docs")
    print("   • Health: http://localhost:9000/health")
    print()
    print("📋 KEY ENDPOINTS:")
    print("   • POST /upload_resume - Upload PDF/DOCX")
    print("   • POST /analyze_resume - Analyze resume + job")
    print("   • GET /match_jobs - Find job matches")
    print()
    print("🎯 FEATURES:")
    print("   • AI-powered resume analysis")
    print("   • Skill gap detection")
    print("   • Job matching with fit scores")
    print("   • Course recommendations")
    print("   • Interactive charts and metrics")
    print()
    print("="*60)

def main():
    """Main execution function"""
    print_banner()
    
    # Check requirements
    if not check_requirements():
        print("\n❌ System requirements not met. Please install missing components.")
        input("Press Enter to exit...")
        return
    
    # Install dependencies
    print("\n🚀 Setting up AI Resume Analyzer...")
    
    if not install_backend_deps():
        print("⚠️  Backend setup failed, trying to continue...")
    
    if not install_frontend_deps():
        print("⚠️  Frontend setup failed, trying to continue...")
    
    # Create directories
    create_directories()
    
    print("\n" + "="*60)
    print("✅ Setup completed successfully!")
    print("="*60)
    
    show_access_info()
    
    # Ask user what to start
    print("\n🚀 What would you like to start?")
    print("1. Full Stack (Backend + Frontend) - Recommended")
    print("2. Backend Only (FastAPI on port 9000)")
    print("3. Frontend Only (React on port 5173)")
    print("4. Exit")
    
    try:
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            print("\n🚀 Starting Full Stack Application...")
            print("📍 Backend: http://localhost:9000")
            print("📍 Frontend: http://localhost:5173")
            print("\nStarting backend first, then frontend...")
            
            # Start backend in a separate thread
            backend_thread = threading.Thread(target=start_backend, daemon=True)
            backend_thread.start()
            
            # Wait a moment for backend to start
            time.sleep(5)
            
            # Test backend
            test_backend()
            
            # Start frontend (this will block)
            print("\n🎨 Starting frontend...")
            start_frontend()
            
        elif choice == '2':
            print("\n🔧 Starting Backend Only...")
            start_backend()
            
        elif choice == '3':
            print("\n🎨 Starting Frontend Only...")
            print("⚠️  Make sure backend is running on port 9000")
            start_frontend()
            
        elif choice == '4':
            print("👋 Goodbye!")
            
        else:
            print("❌ Invalid choice. Starting full stack by default...")
            # Start full stack
            backend_thread = threading.Thread(target=start_backend, daemon=True)
            backend_thread.start()
            time.sleep(5)
            test_backend()
            start_frontend()
            
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
