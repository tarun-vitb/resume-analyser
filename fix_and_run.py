#!/usr/bin/env python3
"""
Fix All Errors and Run Locally - AI Resume Analyzer
Comprehensive script to fix common issues and start the application
"""

import os
import sys
import subprocess
import platform
import time
from pathlib import Path

def print_banner():
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║           🔧 AI Resume Analyzer - Fix & Run Script          ║
║                                                              ║
║              Fixing all errors and starting locally         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)

def run_command(command, description, check=True):
    """Run a command with error handling"""
    print(f"⏳ {description}...")
    try:
        if isinstance(command, str):
            result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        else:
            result = subprocess.run(command, check=check, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ {description} - Success")
            return True
        else:
            print(f"⚠️  {description} - Warning: {result.stderr}")
            return False
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed: {e}")
        return False
    except Exception as e:
        print(f"❌ {description} - Error: {e}")
        return False

def check_python_version():
    """Check Python version"""
    print("\n🐍 Checking Python version...")
    version = sys.version_info
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required. Current: {version.major}.{version.minor}")
        print("Please install Python 3.8 or higher from https://python.org")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    return True

def upgrade_pip():
    """Upgrade pip to latest version"""
    print("\n📦 Upgrading pip...")
    return run_command([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'], "Pip upgrade", check=False)

def install_core_dependencies():
    """Install core dependencies with error handling"""
    print("\n📦 Installing core dependencies...")
    
    core_packages = [
        'fastapi==0.104.1',
        'uvicorn[standard]==0.24.0',
        'python-multipart==0.0.6',
        'pydantic==2.5.0'
    ]
    
    success = True
    for package in core_packages:
        if not run_command([sys.executable, '-m', 'pip', 'install', package], f"Installing {package}", check=False):
            success = False
    
    return success

def install_optional_dependencies():
    """Install optional dependencies for document processing"""
    print("\n📄 Installing document processing libraries...")
    
    optional_packages = [
        'PyPDF2==3.0.1',
        'python-docx==0.8.11',
        'requests==2.31.0',
        'python-dotenv==1.0.0'
    ]
    
    for package in optional_packages:
        run_command([sys.executable, '-m', 'pip', 'install', package], f"Installing {package}", check=False)

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating project directories...")
    
    directories = [
        'uploads',
        'cache', 
        'logs',
        'static',
        'temp'
    ]
    
    for directory in directories:
        try:
            Path(directory).mkdir(parents=True, exist_ok=True)
            print(f"✅ Created {directory}/")
        except Exception as e:
            print(f"⚠️  Could not create {directory}/: {e}")

def fix_import_issues():
    """Fix common import issues"""
    print("\n🔧 Fixing import issues...")
    
    # Create __init__.py files if missing
    core_dir = Path('core')
    if core_dir.exists():
        init_file = core_dir / '__init__.py'
        if not init_file.exists():
            init_file.touch()
            print("✅ Created core/__init__.py")

def test_imports():
    """Test if critical imports work"""
    print("\n🧪 Testing critical imports...")
    
    critical_imports = [
        ('fastapi', 'FastAPI'),
        ('uvicorn', 'Uvicorn'),
        ('pydantic', 'Pydantic')
    ]
    
    all_good = True
    for module, name in critical_imports:
        try:
            __import__(module)
            print(f"✅ {name} import - OK")
        except ImportError as e:
            print(f"❌ {name} import - Failed: {e}")
            all_good = False
    
    return all_good

def check_port_availability():
    """Check if port 8000 is available"""
    print("\n🔌 Checking port availability...")
    
    import socket
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', 8000))
            print("✅ Port 8000 is available")
            return True
    except OSError:
        print("⚠️  Port 8000 is in use. The server might already be running.")
        return False

def create_simple_env():
    """Create a simple .env file"""
    print("\n⚙️  Creating environment configuration...")
    
    env_content = """# AI Resume Analyzer Configuration
DEBUG=True
LOG_LEVEL=INFO
API_HOST=0.0.0.0
API_PORT=8000
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Created .env file")
    except Exception as e:
        print(f"⚠️  Could not create .env file: {e}")

def start_server():
    """Start the simplified server"""
    print("\n🚀 Starting AI Resume Analyzer...")
    print("=" * 60)
    print("📍 Server URL: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("💚 Health Check: http://localhost:8000/health")
    print("🎯 Demo Endpoint: http://localhost:8000/api/v1/demo")
    print("=" * 60)
    print("\n⏳ Starting server... (Press Ctrl+C to stop)")
    
    try:
        # Try to start the simplified version
        subprocess.run([sys.executable, 'simple_main.py'])
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except FileNotFoundError:
        print("❌ simple_main.py not found. Trying alternative method...")
        try:
            subprocess.run([
                sys.executable, '-m', 'uvicorn', 
                'simple_main:app',
                '--host', '0.0.0.0',
                '--port', '8000',
                '--reload'
            ])
        except Exception as e:
            print(f"❌ Failed to start server: {e}")

def run_tests():
    """Run API tests"""
    print("\n🧪 Running API tests...")
    
    # Wait a moment for server to start
    time.sleep(3)
    
    try:
        subprocess.run([sys.executable, 'test_api.py'], timeout=30)
    except subprocess.TimeoutExpired:
        print("⚠️  Tests timed out")
    except FileNotFoundError:
        print("⚠️  Test script not found")
    except Exception as e:
        print(f"⚠️  Test error: {e}")

def main():
    """Main execution function"""
    print_banner()
    
    # Step 1: Check Python version
    if not check_python_version():
        input("Press Enter to exit...")
        return
    
    # Step 2: Upgrade pip
    upgrade_pip()
    
    # Step 3: Install core dependencies
    if not install_core_dependencies():
        print("\n❌ Failed to install core dependencies. Please check your internet connection.")
        input("Press Enter to continue anyway...")
    
    # Step 4: Install optional dependencies
    install_optional_dependencies()
    
    # Step 5: Create directories
    create_directories()
    
    # Step 6: Fix import issues
    fix_import_issues()
    
    # Step 7: Test imports
    if not test_imports():
        print("\n❌ Critical imports failed. Please install missing packages manually.")
        print("Run: pip install fastapi uvicorn python-multipart pydantic")
        input("Press Enter to continue anyway...")
    
    # Step 8: Check port availability
    check_port_availability()
    
    # Step 9: Create environment file
    create_simple_env()
    
    print("\n" + "=" * 60)
    print("✅ Setup completed! Ready to start the server.")
    print("=" * 60)
    
    # Ask user what to do
    print("\nWhat would you like to do?")
    print("1. Start the server")
    print("2. Run tests only")
    print("3. Start server and run tests")
    print("4. Exit")
    
    try:
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            start_server()
        elif choice == '2':
            print("Starting server in background for tests...")
            # Start server in background and run tests
            import threading
            server_thread = threading.Thread(target=start_server, daemon=True)
            server_thread.start()
            time.sleep(5)  # Wait for server to start
            run_tests()
        elif choice == '3':
            print("Starting server and tests...")
            import threading
            server_thread = threading.Thread(target=start_server, daemon=True)
            server_thread.start()
            time.sleep(5)  # Wait for server to start
            run_tests()
            input("\nPress Enter to stop the server...")
        elif choice == '4':
            print("👋 Goodbye!")
        else:
            print("Invalid choice. Starting server by default...")
            start_server()
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
