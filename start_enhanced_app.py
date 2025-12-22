"""
Enhanced AI Resume Analyzer Startup Script
Starts the enhanced backend with full functionality
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
        print("Packages installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error installing packages: {e}")
        return False
    return True

def start_enhanced_application():
    """Start the Enhanced AI Resume Analyzer application"""
    print("\nStarting Enhanced AI Resume Analyzer...")
    print("=" * 50)
    
    # Check if enhanced_backend.py exists
    backend_file = Path("enhanced_backend.py")
    if not backend_file.exists():
        print("Enhanced backend file not found!")
        return False
    
    # Check if static directory exists
    static_dir = Path("static")
    if not static_dir.exists():
        print("Static directory not found!")
        return False
    
    print("All files found!")
    print("\nStarting enhanced backend server...")
    print("   Backend will run on: http://localhost:9001")
    print("   Frontend will be available at: http://localhost:9001")
    print("\nFeatures enabled:")
    print("   - Exact skill name matching")
    print("   - Real company job data (Google, Microsoft, Amazon, etc.)")
    print("   - Accurate percentage calculations")
    print("   - Category-wise skill analysis")
    print("   - Real-time job matching")
    print("\nOpening browser in 3 seconds...")
    
    # Start the backend server
    try:
        # Open browser after a short delay
        def open_browser():
            time.sleep(3)
            webbrowser.open("http://localhost:9001")
        
        import threading
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.start()
        
        # Start the server
        subprocess.run([sys.executable, "enhanced_backend.py"])
        
    except KeyboardInterrupt:
        print("\n\nApplication stopped by user")
    except Exception as e:
        print(f"\nError starting application: {e}")

def main():
    """Main function"""
    print("Enhanced AI Resume Analyzer - Startup Script")
    print("=" * 50)
    
    # Install requirements
    if not install_requirements():
        print("\nFailed to install requirements. Please install manually:")
        print("   pip install fastapi uvicorn python-multipart requests")
        return
    
    # Start application
    start_enhanced_application()

if __name__ == "__main__":
    main()
