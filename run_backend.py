"""Simplified backend startup script with error handling"""

import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed"""
    required = ['fastapi', 'uvicorn']
    missing = []
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"\n❌ Missing required packages: {', '.join(missing)}")
        print("Install them with: pip install -r requirements.txt")
        return False
    return True

def main():
    print("="*70)
    print("Starting AI Resume Analyzer Backend")
    print("="*70)
    
    # Check if main.py exists
    if not Path("main.py").exists():
        print("\n❌ Error: main.py not found!")
        print("Please make sure you're in the correct directory.")
        sys.exit(1)
    
    # Check dependencies
    print("\n📦 Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    
    print("✅ Dependencies OK")
    
    # Try to start the server
    print("\n🚀 Starting backend server on port 9002...")
    print("   Access at: http://localhost:9002")
    print("   API Docs: http://localhost:9002/docs")
    print("\n   Press Ctrl+C to stop\n")
    
    try:
        # Run main.py
        subprocess.run([sys.executable, "main.py"], check=True)
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error starting server: {e}")
        print("\nCommon fixes:")
        print("1. Check if port 9002 is already in use")
        print("2. Install missing dependencies: pip install -r requirements.txt")
        print("3. Check for syntax errors in main.py")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

