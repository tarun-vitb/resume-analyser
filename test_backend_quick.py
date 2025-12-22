"""
Quick Backend Test Script
Test the backend endpoints to identify issues
"""

import requests
import json
import os
from pathlib import Path

def test_backend():
    base_url = "http://localhost:9000"
    
    print("Testing AI Resume Analyzer Backend...")
    print("=" * 50)
    
    # Test 1: Health check
    print("1. Testing health check...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 2: Upload resume
    print("\n2. Testing resume upload...")
    
    # Create a simple test resume file
    test_resume_path = Path("test_resume_quick.txt")
    test_resume_content = """
John Doe
Software Engineer
Email: john.doe@email.com
Phone: (555) 123-4567

SKILLS:
- Python
- JavaScript
- React
- FastAPI
- Machine Learning
- Data Analysis

EXPERIENCE:
Software Engineer at Tech Company (2020-2023)
- Developed web applications using React and Python
- Implemented machine learning models
- Worked with databases and APIs

EDUCATION:
Bachelor of Science in Computer Science
University of Technology (2016-2020)
"""
    
    with open(test_resume_path, 'w') as f:
        f.write(test_resume_content)
    
    try:
        with open(test_resume_path, 'rb') as f:
            files = {'file': ('test_resume.txt', f, 'text/plain')}
            response = requests.post(f"{base_url}/upload_resume", files=files)
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}")
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    file_id = result.get('file_id')
                    print(f"   File ID: {file_id}")
                    
                    # Test 3: Analyze resume
                    print("\n3. Testing resume analysis...")
                    job_description = """
We are looking for a Senior Software Engineer with experience in:
- Python programming
- Web development with React
- API development with FastAPI
- Machine learning and data science
- Database management
- Cloud platforms (AWS/Azure)
"""
                    
                    analysis_data = {
                        'file_id': file_id,
                        'job_description': job_description
                    }
                    
                    analysis_response = requests.post(f"{base_url}/analyze_resume", data=analysis_data)
                    print(f"   Status: {analysis_response.status_code}")
                    print(f"   Response: {analysis_response.json()}")
                    
                    # Test 4: Job matches
                    print("\n4. Testing job matches...")
                    matches_response = requests.get(f"{base_url}/match_jobs?file_id={file_id}")
                    print(f"   Status: {matches_response.status_code}")
                    print(f"   Response: {matches_response.json()}")
                    
    except Exception as e:
        print(f"   Error: {e}")
    finally:
        # Clean up test file
        if test_resume_path.exists():
            test_resume_path.unlink()
    
    print("\n" + "=" * 50)
    print("Backend test completed!")

if __name__ == "__main__":
    test_backend()
