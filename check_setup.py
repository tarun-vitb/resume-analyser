"""Diagnostic script to check setup and identify issues"""

import sys
import os
from pathlib import Path

print("="*70)
print("AI Resume Analyzer - Setup Diagnostic")
print("="*70)

# Check Python version
print("\n1. Python Version:")
print(f"   {sys.version}")

# Check if main.py exists
print("\n2. Checking main.py:")
if Path("main.py").exists():
    print("   ✅ main.py exists")
    try:
        with open("main.py", "r", encoding="utf-8") as f:
            content = f.read()
            if "from fastapi import" in content:
                print("   ✅ Contains FastAPI imports")
            if "app = FastAPI" in content:
                print("   ✅ Contains FastAPI app definition")
    except Exception as e:
        print(f"   ❌ Error reading main.py: {e}")
else:
    print("   ❌ main.py not found!")

# Check core modules
print("\n3. Checking core modules:")
core_dir = Path("core")
if core_dir.exists():
    print("   ✅ core/ directory exists")
    required_modules = [
        "document_processor.py",
        "nlp_engine.py", 
        "skill_analyzer.py",
        "prediction_model.py"
    ]
    for module in required_modules:
        if (core_dir / module).exists():
            print(f"   ✅ {module} exists")
        else:
            print(f"   ❌ {module} missing")
else:
    print("   ❌ core/ directory not found!")

# Check Python dependencies
print("\n4. Checking Python dependencies:")
required_packages = [
    "fastapi",
    "uvicorn",
    "pydantic",
    "numpy",
    "sentence_transformers"
]

for package in required_packages:
    try:
        __import__(package.replace("-", "_"))
        print(f"   ✅ {package}")
    except ImportError:
        print(f"   ❌ {package} - NOT INSTALLED")

# Check frontend
print("\n5. Checking frontend:")
frontend_dir = Path("frontend-app")
if frontend_dir.exists():
    print("   ✅ frontend-app/ directory exists")
    if (frontend_dir / "package.json").exists():
        print("   ✅ package.json exists")
    else:
        print("   ❌ package.json missing")
    
    if (frontend_dir / "node_modules").exists():
        print("   ✅ node_modules exists (dependencies installed)")
    else:
        print("   ⚠️  node_modules missing - run 'npm install' in frontend-app/")
else:
    print("   ❌ frontend-app/ directory not found!")

# Try to import main.py
print("\n6. Testing main.py import:")
try:
    import main
    print("   ✅ main.py imports successfully!")
    if hasattr(main, 'app'):
        print(f"   ✅ FastAPI app object: {main.app.title}")
    if hasattr(main, 'uploaded_resume_data'):
        print("   ✅ uploaded_resume_data global variable exists")
except SyntaxError as e:
    print(f"   ❌ Syntax Error: {e}")
    print(f"   Line: {e.lineno}, Text: {e.text}")
except ImportError as e:
    print(f"   ❌ Import Error: {e}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
print("Diagnostic complete!")
print("="*70)

