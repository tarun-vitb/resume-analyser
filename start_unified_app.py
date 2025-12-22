"""
Unified Startup Script for AI Resume Analyzer
Starts both backend (FastAPI) and frontend (React) together
"""

import subprocess
import threading
import time
import sys
import webbrowser
from pathlib import Path

def print_banner():
    """Print startup banner"""
    print("\n" + "="*70)
    print("🤖 AI RESUME ANALYZER - UNIFIED APPLICATION")
    print("="*70)
    print("🚀 Starting complete application...")
    print("   • Backend (FastAPI): http://localhost:9002")
    print("   • Frontend (React): http://localhost:5174")
    print("   • API Docs: http://localhost:9002/docs")
    print("="*70 + "\n")

def check_requirements():
    """Check if required files and dependencies exist"""
    errors = []
    
    # Check backend file
    if not Path("main.py").exists():
        errors.append("✗ Backend file (main.py) not found!")
    
    # Check frontend directory
    if not Path("frontend-app").exists():
        errors.append("✗ Frontend directory (frontend-app) not found!")
    
    # Check Python
    try:
        subprocess.run([sys.executable, "--version"], capture_output=True, check=True)
    except:
        errors.append("✗ Python not found!")
    
    # Check Node.js
    try:
        subprocess.run(["node", "--version"], capture_output=True, check=True)
    except:
        errors.append("✗ Node.js not found! Please install Node.js to run the frontend.")
    
    if errors:
        print("\n❌ Setup Issues Found:")
        for error in errors:
            print(f"   {error}")
        return False
    
    return True

def install_python_dependencies():
    """Install Python dependencies"""
    print("📦 Checking Python dependencies...")
    try:
        # Try to import key packages
        import fastapi
        import uvicorn
        print("   ✓ Python dependencies already installed")
        return True
    except ImportError:
        print("   ⚠ Installing Python dependencies...")
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                check=True,
                capture_output=True
            )
            print("   ✓ Python dependencies installed")
            return True
        except subprocess.CalledProcessError as e:
            print(f"   ✗ Failed to install Python dependencies: {e}")
            return False

def install_node_dependencies():
    """Install Node.js dependencies"""
    frontend_path = Path("frontend-app")
    node_modules = frontend_path / "node_modules"
    
    if node_modules.exists():
        print("   ✓ Node.js dependencies already installed")
        return True
    
    print("   ⚠ Installing Node.js dependencies (this may take a minute)...")
    try:
        subprocess.run(
            ["npm", "install"],
            cwd=frontend_path,
            check=True,
            capture_output=True
        )
        print("   ✓ Node.js dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ✗ Failed to install Node.js dependencies: {e}")
        print("   Try running 'npm install' manually in the frontend-app directory")
        return False
    except FileNotFoundError:
        print("   ✗ npm not found. Please install Node.js")
        return False

def start_backend():
    """Start the FastAPI backend server"""
    print("\n🔧 Starting backend server on port 9002...")
    try:
        subprocess.run(
            [sys.executable, "main.py"],
            check=True
        )
    except KeyboardInterrupt:
        print("\n🛑 Backend stopped")
    except Exception as e:
        print(f"❌ Backend error: {e}")

def start_frontend():
    """Start the React frontend"""
    frontend_path = Path("frontend-app")
    print("\n🎨 Starting frontend on port 5174...")
    try:
        subprocess.run(
            ["npm", "run", "dev"],
            cwd=frontend_path,
            check=True
        )
    except KeyboardInterrupt:
        print("\n🛑 Frontend stopped")
    except Exception as e:
        print(f"❌ Frontend error: {e}")

def open_browser_delayed():
    """Open browser after services start"""
    time.sleep(5)  # Wait for servers to start
    print("\n🌐 Opening browser...")
    try:
        webbrowser.open("http://localhost:5174")
    except:
        pass

def main():
    """Main function"""
    print_banner()
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Please fix the issues above and try again.")
        sys.exit(1)
    
    # Install dependencies
    print("\n📦 Checking dependencies...")
    install_python_dependencies()
    install_node_dependencies()
    
    # Start browser opener in background
    browser_thread = threading.Thread(target=open_browser_delayed, daemon=True)
    browser_thread.start()
    
    # Start backend in background thread
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    print("✓ Backend starting on http://localhost:9002")
    print("✓ Frontend starting on http://localhost:5174")
    print("\n⏳ Waiting for services to start...")
    time.sleep(3)
    
    print("\n" + "="*70)
    print("✅ Application is running!")
    print("   📍 Frontend: http://localhost:5174")
    print("   📍 Backend API: http://localhost:9002")
    print("   📍 API Docs: http://localhost:9002/docs")
    print("\n   Press Ctrl+C to stop both servers")
    print("="*70 + "\n")
    
    # Start frontend (this will block)
    try:
        start_frontend()
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping application...")
        print("👋 Goodbye!")

if __name__ == "__main__":
    main()

