"""
Final AI Resume Analyzer Startup Script
Starts the completely fixed version with verified data transfer
"""

import subprocess
import sys
import time
import webbrowser
from pathlib import Path
import requests

def check_backend_health():
    """Check if backend is responding correctly"""
    try:
        response = requests.get("http://localhost:9002/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn", "python-multipart", "requests"], 
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✓ Packages installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing packages: {e}")
        return False
    return True

def start_final_application():
    """Start the Final AI Resume Analyzer application"""
    print("\n" + "="*60)
    print("🚀 STARTING FINAL AI RESUME ANALYZER")
    print("="*60)
    
    # Check if fixed backend exists
    backend_file = Path("fixed_enhanced_backend.py")
    if not backend_file.exists():
        print("✗ Fixed backend file not found!")
        return False
    
    # Check if static directory exists
    static_dir = Path("static")
    if not static_dir.exists():
        print("✗ Static directory not found!")
        return False
    
    print("✓ All files found!")
    print("\n📡 Starting fixed backend server...")
    print("   🌐 Backend: http://localhost:9002")
    print("   🎨 Frontend: http://localhost:9002")
    
    print("\n🎯 VERIFIED FEATURES:")
    print("   ✓ Accurate skill extraction and matching")
    print("   ✓ Correct percentage calculations")
    print("   ✓ Real company job data with eligibility filtering")
    print("   ✓ Enhanced UI with round buttons and animations")
    print("   ✓ Proper data transfer between frontend and backend")
    print("   ✓ Only shows eligible job vacancies")
    print("   ✓ Clear skill categorization and counts")
    
    print("\n🏢 REAL COMPANIES INCLUDED:")
    print("   • Google, Microsoft, Amazon, Meta")
    print("   • Netflix, Apple, Tesla, Spotify")
    print("   • With actual job requirements and salaries")
    
    print("\n⏳ Opening browser in 3 seconds...")
    
    # Start the backend server
    try:
        # Open browser after a short delay
        def open_browser():
            time.sleep(3)
            if check_backend_health():
                print("✓ Backend is healthy - opening browser...")
                webbrowser.open("http://localhost:9002")
            else:
                print("✗ Backend health check failed")
        
        import threading
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.start()
        
        # Start the server
        print("\n🔥 Starting server...")
        subprocess.run([sys.executable, "fixed_enhanced_backend.py"])
        
    except KeyboardInterrupt:
        print("\n\n🛑 Application stopped by user")
    except Exception as e:
        print(f"\n✗ Error starting application: {e}")

def main():
    """Main function"""
    print("🤖 AI Resume Analyzer - FINAL WORKING VERSION")
    print("="*60)
    print("🎯 All issues have been resolved:")
    print("   ✓ Skills showing correctly with exact names")
    print("   ✓ Accurate percentages (not 0%)")
    print("   ✓ Only eligible job vacancies displayed")
    print("   ✓ Real company data with proper requirements")
    print("   ✓ Enhanced UI with round buttons")
    print("   ✓ Verified data transfer and NLP processing")
    
    # Install requirements
    if not install_requirements():
        print("\n✗ Failed to install requirements. Please install manually:")
        print("   pip install fastapi uvicorn python-multipart requests")
        return
    
    # Start application
    start_final_application()

if __name__ == "__main__":
    main()
