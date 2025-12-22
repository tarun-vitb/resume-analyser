"""Simplified frontend startup script with error handling"""

import sys
import subprocess
from pathlib import Path

def main():
    print("="*70)
    print("Starting AI Resume Analyzer Frontend")
    print("="*70)
    
    frontend_dir = Path("frontend-app")
    
    # Check if frontend directory exists
    if not frontend_dir.exists():
        print("\n❌ Error: frontend-app directory not found!")
        print("Please make sure you're in the correct directory.")
        sys.exit(1)
    
    # Check if package.json exists
    if not (frontend_dir / "package.json").exists():
        print("\n❌ Error: package.json not found in frontend-app!")
        sys.exit(1)
    
    # Check if node_modules exists
    if not (frontend_dir / "node_modules").exists():
        print("\n⚠️  node_modules not found. Installing dependencies...")
        try:
            subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
            print("✅ Dependencies installed")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            print("Try running manually: cd frontend-app && npm install")
            sys.exit(1)
        except FileNotFoundError:
            print("❌ npm not found. Please install Node.js")
            sys.exit(1)
    
    print("\n🚀 Starting frontend server on port 5174...")
    print("   Access at: http://localhost:5174")
    print("\n   Press Ctrl+C to stop\n")
    
    try:
        subprocess.run(["npm", "run", "dev"], cwd=frontend_dir, check=True)
    except KeyboardInterrupt:
        print("\n\n🛑 Frontend stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error starting frontend: {e}")
        print("\nCommon fixes:")
        print("1. Install dependencies: cd frontend-app && npm install")
        print("2. Check if port 5174 is already in use")
        sys.exit(1)
    except FileNotFoundError:
        print("\n❌ npm not found. Please install Node.js")
        sys.exit(1)

if __name__ == "__main__":
    main()

