"""
Simple Application Startup Script
Starts the AI Resume Analyzer with all components integrated
"""

import subprocess
import sys
import time
import webbrowser
from pathlib import Path

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn", "python-multipart", "requests"])
        print("✅ Packages installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False
    return True

def start_application():
    """Start the AI Resume Analyzer application"""
    print("\n🚀 Starting AI Resume Analyzer...")
    print("=" * 50)
    
    # Check if clean_backend.py exists
    backend_file = Path("clean_backend.py")
    if not backend_file.exists():
        print("❌ Backend file not found!")
        return False
    
    # Check if static directory exists
    static_dir = Path("static")
    if not static_dir.exists():
        print("❌ Static directory not found!")
        return False
    
    print("✅ All files found!")
    print("\n📡 Starting backend server...")
    print("   Backend will run on: http://localhost:9000")
    print("   Frontend will be available at: http://localhost:9000")
    print("\n🌐 Opening browser in 3 seconds...")
    
    # Start the backend server
    try:
        # Open browser after a short delay
        def open_browser():
            time.sleep(3)
            webbrowser.open("http://localhost:9000")
        
        import threading
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.start()
        
        # Start the server
        subprocess.run([sys.executable, "clean_backend.py"])
        
    except KeyboardInterrupt:
        print("\n\n🛑 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")

def main():
    """Main function"""
    print("🤖 AI Resume Analyzer - Startup Script")
    print("=" * 50)
    
    # Install requirements
    if not install_requirements():
        print("\n❌ Failed to install requirements. Please install manually:")
        print("   pip install fastapi uvicorn python-multipart requests")
        return
    
    # Start application
    start_application()

if __name__ == "__main__":
    main()
