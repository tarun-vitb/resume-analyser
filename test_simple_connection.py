"""
Simple Connection Test - No Unicode
"""

import requests
from pathlib import Path

def test_simple_connection():
    base_url = "http://localhost:9002"
    
    print("TESTING REACT FRONTEND CONNECTION")
    print("="*50)
    
    # Test health
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("Backend is healthy")
        else:
            print(f"Backend health failed: {response.status_code}")
            return
    except Exception as e:
        print(f"Cannot connect to backend: {e}")
        print("Start backend with: python fixed_enhanced_backend.py")
        return
    
    # Test upload
    test_resume = """
JOHN DOE
Software Developer
SKILLS: Python, JavaScript, React, Machine Learning, AWS
"""
    
    test_file = Path("test_simple.txt")
    
    try:
        with open(test_file, 'w') as f:
            f.write(test_resume)
        
        with open(test_file, 'rb') as f:
            files = {'file': ('test_simple.txt', f, 'text/plain')}
            response = requests.post(f"{base_url}/upload_resume", files=files)
        
        print(f"Upload Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            extracted_skills = result.get('extracted_skills', [])
            print(f"SUCCESS: {len(extracted_skills)} skills extracted")
            print(f"Skills: {extracted_skills}")
            
            if len(extracted_skills) > 0:
                print("SKILLS EXTRACTION WORKING!")
            else:
                print("ERROR: No skills extracted")
        else:
            print(f"Upload failed: {response.text}")
    
    except Exception as e:
        print(f"Test error: {e}")
    
    finally:
        if test_file.exists():
            test_file.unlink()
    
    print("\nNEXT STEPS:")
    print("1. Backend: python fixed_enhanced_backend.py")
    print("2. Frontend: python start_react_app.py")
    print("3. Open: http://localhost:5173")

if __name__ == "__main__":
    test_simple_connection()
