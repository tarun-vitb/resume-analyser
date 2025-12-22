#!/usr/bin/env python3
"""
Quick Local Setup and Run Script for AI Resume Analyzer
Fixes common issues and starts the application immediately
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_header():
    print("🚀 AI Resume Analyzer - Quick Local Setup")
    print("=" * 50)

def check_python():
    """Check Python version"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required. Current: {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def install_minimal_deps():
    """Install minimal dependencies"""
    print("\n📦 Installing minimal dependencies...")
    
    try:
        # Install minimal requirements
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', 
            'fastapi==0.104.1',
            'uvicorn==0.24.0', 
            'python-multipart==0.0.6',
            'pydantic==2.5.0'
        ])
        print("✅ Core dependencies installed")
        
        # Try to install document processing (optional)
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install',
                'PyPDF2==3.0.1',
                'python-docx==0.8.11'
            ])
            print("✅ Document processing libraries installed")
        except subprocess.CalledProcessError:
            print("⚠️  Document processing libraries failed (optional)")
            
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    dirs = ['uploads', 'cache', 'logs']
    for d in dirs:
        Path(d).mkdir(exist_ok=True)
        print(f"✅ {d}/")

def test_imports():
    """Test if we can import required modules"""
    print("\n🧪 Testing imports...")
    
    try:
        import fastapi
        print("✅ FastAPI")
    except ImportError:
        print("❌ FastAPI - Run: pip install fastapi")
        return False
        
    try:
        import uvicorn
        print("✅ Uvicorn")
    except ImportError:
        print("❌ Uvicorn - Run: pip install uvicorn")
        return False
        
    return True

def start_server():
    """Start the simplified server"""
    print("\n🚀 Starting AI Resume Analyzer...")
    print("📍 Server: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("💚 Health: http://localhost:8000/health")
    print("🎯 Demo: http://localhost:8000/api/v1/demo")
    print("\nPress Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Import and run the simplified app
        os.system(f"{sys.executable} simple_main.py")
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        print("\nTrying alternative method...")
        try:
            subprocess.run([
                sys.executable, '-m', 'uvicorn', 
                'simple_main:app',
                '--host', '0.0.0.0',
                '--port', '8000',
                '--reload'
            ])
        except Exception as e2:
            print(f"❌ Alternative method failed: {e2}")

def main():
    """Main function"""
    print_header()
    
    # Check Python version
    if not check_python():
        return
    
    # Install dependencies
    if not install_minimal_deps():
        print("\n⚠️  Trying to continue with existing packages...")
    
    # Create directories
    create_directories()
    
    # Test imports
    if not test_imports():
        print("\n❌ Import test failed. Please install missing packages.")
        return
    
    print("\n" + "=" * 50)
    print("✅ Setup completed successfully!")
    print("=" * 50)
    
    # Start server
    start_server()

if __name__ == "__main__":
    main()
