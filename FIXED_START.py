#!/usr/bin/env python3
"""
🚀 FIXED AI Resume Analyzer Startup Script
This version fixes all Windows dependency issues and runs perfectly
"""

import os
import sys
import subprocess
import time
import threading
import webbrowser
from pathlib import Path

def print_banner():
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    🚀 AI RESUME ANALYZER - FIXED VERSION                   ║
║                                                              ║
║    ✅ No complex dependencies (PyMuPDF, scikit-learn)      ║
║    ✅ Works on Windows without Visual Studio               ║
║    ✅ Simple backend with full functionality               ║
║    ✅ Beautiful React frontend                             ║
║                                                              ║
║    Backend:  http://localhost:9000                          ║
║    Frontend: http://localhost:5173                          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)

def check_python():
    """Check Python version"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required. Current: {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_node():
    """Check Node.js"""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✅ Node.js {result.stdout.strip()}")
            return True
        else:
            print("❌ Node.js not found")
            return False
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print("❌ Node.js not found")
        return False

def install_backend_simple():
    """Install only essential backend dependencies"""
    print("📦 Installing backend dependencies (simple version)...")
    
    try:
        # Only install the essential packages that work on Windows
        deps = [
            'fastapi==0.104.1',
            'uvicorn[standard]==0.24.0',
            'python-multipart==0.0.6',
            'pydantic==2.5.0'
        ]
        
        print("   Installing:", ', '.join(deps))
        
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install'
        ] + deps, capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print("✅ Backend dependencies installed successfully")
            return True
        else:
            print(f"⚠️  Some packages may have failed, but continuing...")
            print(f"   Error: {result.stderr[:200]}...")
            return True  # Continue anyway
            
    except subprocess.TimeoutExpired:
        print("⚠️  Installation timed out, but continuing...")
        return True
    except Exception as e:
        print(f"⚠️  Installation error: {e}")
        return True

def install_frontend():
    """Install frontend dependencies"""
    print("📦 Installing frontend dependencies...")
    
    frontend_dir = Path('frontend-app')
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    try:
        os.chdir(frontend_dir)
        
        print("   Running npm install...")
        result = subprocess.run(['npm', 'install'], 
                              capture_output=True, text=True, timeout=180)
        
        if result.returncode == 0:
            print("✅ Frontend dependencies installed")
            os.chdir('..')
            return True
        else:
            print(f"⚠️  Frontend installation had issues: {result.stderr[:200]}...")
            os.chdir('..')
            return True  # Continue anyway
            
    except subprocess.TimeoutExpired:
        print("⚠️  Frontend installation timed out")
        os.chdir('..')
        return True
    except FileNotFoundError:
        print("❌ npm not found - Node.js may not be installed")
        os.chdir('..')
        return False
    except Exception as e:
        print(f"❌ Frontend installation error: {e}")
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
    """Start the simple backend"""
    print("🔧 Starting backend server...")
    try:
        # Use the simple backend that doesn't require complex dependencies
        subprocess.run([sys.executable, 'simple_backend.py'])
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
    """Test if backend is working"""
    print("🧪 Testing backend...")
    time.sleep(4)  # Wait for backend to start
    
    try:
        import urllib.request
        response = urllib.request.urlopen('http://localhost:9000/health', timeout=10)
        if response.getcode() == 200:
            print("✅ Backend is running and healthy")
            return True
        else:
            print(f"⚠️  Backend responded with status {response.getcode()}")
            return False
    except Exception as e:
        print(f"❌ Backend test failed: {e}")
        return False

def open_browser():
    """Open browser after servers start"""
    time.sleep(10)  # Wait for both servers
    try:
        webbrowser.open('http://localhost:5173')
        print("🌐 Opened browser to http://localhost:5173")
    except Exception as e:
        print(f"⚠️  Could not open browser automatically: {e}")

def show_instructions():
    """Show usage instructions"""
    print("\n" + "="*60)
    print("🎯 AI RESUME ANALYZER - READY TO USE!")
    print("="*60)
    print()
    print("🌐 ACCESS POINTS:")
    print("   • Frontend:     http://localhost:5173")
    print("   • Backend API:  http://localhost:9000")
    print("   • API Docs:     http://localhost:9000/docs")
    print("   • Health Check: http://localhost:9000/health")
    print()
    print("📋 HOW TO USE:")
    print("   1. Go to http://localhost:5173")
    print("   2. Click 'Analyze' in the navigation")
    print("   3. Upload a resume file (PDF/DOCX/TXT)")
    print("   4. Enter a job description")
    print("   5. Click 'Analyze Resume'")
    print("   6. View interactive results with charts")
    print("   7. Check 'Matches' page for job recommendations")
    print()
    print("🎨 FEATURES:")
    print("   ✅ Drag & drop file upload")
    print("   ✅ AI-powered resume analysis")
    print("   ✅ Interactive charts and visualizations")
    print("   ✅ Skill gap detection")
    print("   ✅ Job matching with fit scores")
    print("   ✅ Course recommendations")
    print("   ✅ Responsive design with animations")
    print()
    print("🔧 TECH STACK:")
    print("   • Backend:  FastAPI + Python (simple version)")
    print("   • Frontend: React + Vite + Tailwind CSS")
    print("   • Charts:   Recharts for data visualization")
    print("   • Icons:    Heroicons")
    print("   • Animations: Framer Motion")
    print()
    print("📄 SAMPLE FILES:")
    print("   • A sample_resume.txt file will be created")
    print("   • You can upload this for testing")
    print("   • Supports PDF, DOCX, and TXT files")
    print()
    print("="*60)

def create_sample_resume():
    """Create a sample resume file for testing"""
    sample_content = """John Doe
Senior Software Engineer
Email: john.doe@email.com
Phone: (555) 123-4567

SKILLS:
Python, JavaScript, React, Node.js, SQL, Git, Docker, AWS, HTML, CSS, MongoDB, PostgreSQL, FastAPI, Express.js, Machine Learning, Data Analysis

EXPERIENCE:
Senior Software Engineer | TechCorp Solutions | 2021-2024
• Developed and maintained web applications using React and Python
• Built RESTful APIs with FastAPI and Node.js
• Managed databases including PostgreSQL and MongoDB
• Deployed applications on AWS cloud infrastructure
• Led a team of 4 junior developers
• Implemented CI/CD pipelines using Docker and Jenkins
• Improved application performance by 40%

Software Developer | StartupXYZ | 2019-2021
• Created responsive web interfaces using React and JavaScript
• Developed backend services with Python and Express.js
• Worked with SQL databases and performed data analysis
• Collaborated with cross-functional teams in Agile environment
• Implemented user authentication and authorization systems

Junior Developer | WebDev Inc | 2018-2019
• Built websites using HTML, CSS, and JavaScript
• Learned Python programming and web frameworks
• Assisted in database design and optimization
• Participated in code reviews and testing

EDUCATION:
Bachelor of Computer Science | University of Technology | 2014-2018
• Relevant coursework: Data Structures, Algorithms, Database Systems, Web Development
• GPA: 3.8/4.0
• Senior project: E-commerce platform using React and Python

PROJECTS:
E-commerce Platform
• Full-stack web application with React frontend and FastAPI backend
• Integrated payment processing using Stripe API
• Implemented user authentication and product management
• Deployed using Docker containers on AWS

Data Analytics Dashboard
• Python application for processing and visualizing large datasets
• Used Pandas and NumPy for statistical analysis
• Created interactive charts with Matplotlib and Plotly
• Automated report generation and email notifications

CERTIFICATIONS:
• AWS Certified Solutions Architect
• Google Cloud Professional Developer
• MongoDB Certified Developer
"""
    
    with open("sample_resume.txt", "w") as f:
        f.write(sample_content)
    
    print("📄 Created sample_resume.txt for testing")

def main():
    """Main execution function"""
    print_banner()
    
    # System checks
    print("🔍 Checking system requirements...")
    if not check_python():
        input("Press Enter to exit...")
        return
    
    node_available = check_node()
    if not node_available:
        print("⚠️  Node.js not found. Frontend may not work.")
        print("   Please install Node.js from https://nodejs.org")
        choice = input("Continue anyway? (y/n): ").lower()
        if choice != 'y':
            return
    
    # Setup
    print("\n🚀 Setting up AI Resume Analyzer...")
    
    create_directories()
    create_sample_resume()
    
    # Install dependencies
    backend_ok = install_backend_simple()
    frontend_ok = install_frontend() if node_available else False
    
    if not backend_ok:
        print("❌ Backend setup failed")
        input("Press Enter to exit...")
        return
    
    if not frontend_ok and node_available:
        print("⚠️  Frontend setup had issues, but continuing...")
    
    # Show instructions
    show_instructions()
    
    # Start application
    print("🚀 Starting application servers...")
    print("⏳ Backend starting on port 9000...")
    
    # Start backend in background thread
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    # Test backend
    if test_backend():
        print("✅ Backend is ready!")
    else:
        print("❌ Backend test failed")
        input("Press Enter to exit...")
        return
    
    if frontend_ok:
        # Open browser in background
        browser_thread = threading.Thread(target=open_browser, daemon=True)
        browser_thread.start()
        
        print("⏳ Frontend starting on port 5173...")
        print("🌐 Browser will open automatically")
        print("\nPress Ctrl+C to stop both servers")
        print("-" * 60)
        
        # Start frontend (this will block)
        try:
            start_frontend()
        except KeyboardInterrupt:
            print("\n👋 Application stopped by user")
    else:
        print("\n⚠️  Frontend not available. Backend running on http://localhost:9000")
        print("📚 API Documentation: http://localhost:9000/docs")
        print("\nPress Ctrl+C to stop the backend server")
        
        try:
            # Keep the main thread alive
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Application stopped by user")

if __name__ == "__main__":
    main()
