#!/usr/bin/env python3
"""
AI Resume Analyzer Startup Script
Automated setup and launch script for the AI Resume Analyzer platform
"""

import os
import sys
import subprocess
import platform
import time
from pathlib import Path

def print_banner():
    """Print application banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║               🚀 AI Resume Analyzer v2.0                    ║
    ║                                                              ║
    ║        Advanced AI-Powered Career Intelligence Platform      ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("❌ Python 3.9+ is required. Current version:", f"{version.major}.{version.minor}")
        sys.exit(1)
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")

def check_dependencies():
    """Check if required dependencies are installed"""
    print("\n📦 Checking dependencies...")
    
    required_packages = [
        'fastapi', 'uvicorn', 'sentence-transformers', 
        'scikit-learn', 'pandas', 'numpy'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - Missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', 
                '-r', 'requirements.txt'
            ])
            print("✅ Dependencies installed successfully")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies")
            print("Please run: pip install -r requirements.txt")
            sys.exit(1)

def download_models():
    """Download required NLP models"""
    print("\n🧠 Checking NLP models...")
    
    try:
        import spacy
        try:
            spacy.load("en_core_web_sm")
            print("✅ spaCy English model available")
        except OSError:
            print("📥 Downloading spaCy English model...")
            subprocess.check_call([
                sys.executable, '-m', 'spacy', 'download', 'en_core_web_sm'
            ])
            print("✅ spaCy model downloaded")
    except ImportError:
        print("⚠️  spaCy not available, some features may be limited")

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = [
        'uploads', 'cache', 'cache/embeddings', 'cache/models', 
        'logs', 'static'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ {directory}/")

def setup_environment():
    """Setup environment configuration"""
    print("\n⚙️  Setting up environment...")
    
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    if not env_file.exists() and env_example.exists():
        print("📋 Creating .env from .env.example...")
        with open(env_example, 'r') as f:
            content = f.read()
        
        with open(env_file, 'w') as f:
            f.write(content)
        print("✅ .env file created")
    elif env_file.exists():
        print("✅ .env file exists")
    else:
        print("⚠️  No environment configuration found")

def check_ports():
    """Check if required ports are available"""
    print("\n🔌 Checking ports...")
    
    import socket
    
    def is_port_available(port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('localhost', port))
                return True
            except OSError:
                return False
    
    ports_to_check = [8000, 3000]
    
    for port in ports_to_check:
        if is_port_available(port):
            print(f"✅ Port {port} available")
        else:
            print(f"⚠️  Port {port} in use")

def start_backend():
    """Start the FastAPI backend server"""
    print("\n🚀 Starting FastAPI backend server...")
    print("📍 Backend will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔄 Interactive API: http://localhost:8000/redoc")
    
    try:
        # Start the FastAPI server
        subprocess.run([
            sys.executable, '-m', 'uvicorn', 'main:app',
            '--host', '0.0.0.0',
            '--port', '8000',
            '--reload'
        ])
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def start_frontend():
    """Start the React frontend (if available)"""
    frontend_dir = Path('frontend')
    
    if frontend_dir.exists() and (frontend_dir / 'package.json').exists():
        print("\n🎨 Starting React frontend...")
        print("📍 Frontend will be available at: http://localhost:3000")
        
        try:
            os.chdir(frontend_dir)
            
            # Check if node_modules exists
            if not Path('node_modules').exists():
                print("📦 Installing frontend dependencies...")
                subprocess.run(['npm', 'install'], check=True)
            
            # Start the development server
            subprocess.run(['npm', 'start'])
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error starting frontend: {e}")
        except FileNotFoundError:
            print("❌ Node.js/npm not found. Please install Node.js to run the frontend.")
        finally:
            os.chdir('..')
    else:
        print("⚠️  Frontend not found. Running backend only.")

def show_usage_info():
    """Show usage information"""
    print("\n" + "="*60)
    print("🎯 AI RESUME ANALYZER - QUICK START GUIDE")
    print("="*60)
    print()
    print("📋 MAIN FEATURES:")
    print("   • Smart Resume Analysis (PDF/DOCX)")
    print("   • ML-Powered Job Matching")
    print("   • Skill Gap Detection")
    print("   • Personalized Feedback")
    print("   • Upskilling Recommendations")
    print("   • Multi-Job Analysis")
    print()
    print("🌐 ACCESS POINTS:")
    print("   • Backend API: http://localhost:8000")
    print("   • API Docs: http://localhost:8000/docs")
    print("   • Health Check: http://localhost:8000/health")
    print("   • Frontend: http://localhost:3000 (if available)")
    print()
    print("🔧 QUICK COMMANDS:")
    print("   • Test API: curl http://localhost:8000/health")
    print("   • Upload Resume: Use /api/v1/analyze-resume endpoint")
    print("   • Multi-Job Match: Use /api/v1/match-multiple-jobs endpoint")
    print()
    print("📚 DOCUMENTATION:")
    print("   • Full API docs available at /docs endpoint")
    print("   • README.md for detailed setup instructions")
    print("   • Example requests in the documentation")
    print()
    print("🆘 SUPPORT:")
    print("   • Check logs/ directory for error logs")
    print("   • Ensure all dependencies are installed")
    print("   • Verify .env configuration")
    print()
    print("="*60)

def main():
    """Main startup function"""
    print_banner()
    
    # System checks
    check_python_version()
    check_dependencies()
    download_models()
    create_directories()
    setup_environment()
    check_ports()
    
    print("\n" + "="*60)
    print("✅ All checks completed successfully!")
    print("="*60)
    
    show_usage_info()
    
    # Ask user what to start
    print("\n🚀 What would you like to start?")
    print("1. Backend only (FastAPI)")
    print("2. Frontend only (React)")
    print("3. Full stack (Backend + Frontend)")
    print("4. Docker deployment")
    print("5. Exit")
    
    try:
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            start_backend()
        elif choice == '2':
            start_frontend()
        elif choice == '3':
            print("Starting full stack deployment...")
            print("Note: Start backend first, then frontend in separate terminal")
            start_backend()
        elif choice == '4':
            print("\n🐳 Starting Docker deployment...")
            print("Run: docker-compose up --build")
            subprocess.run(['docker-compose', 'up', '--build'])
        elif choice == '5':
            print("👋 Goodbye!")
            sys.exit(0)
        else:
            print("❌ Invalid choice. Starting backend by default...")
            start_backend()
            
    except KeyboardInterrupt:
        print("\n👋 Startup cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Startup error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
