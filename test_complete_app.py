#!/usr/bin/env python3
"""
Complete Application Test Suite
Tests all components of the AI Resume Analyzer
"""

import requests
import json
import time
import os
from pathlib import Path

BASE_URL = "http://localhost:9000"
FRONTEND_URL = "http://localhost:5173"

def test_backend_health():
    """Test backend health endpoint"""
    print("🔍 Testing backend health...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend healthy - Status: {data.get('status')}")
            return True
        else:
            print(f"❌ Backend unhealthy - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend health check failed: {e}")
        return False

def test_frontend_access():
    """Test frontend accessibility"""
    print("🔍 Testing frontend access...")
    try:
        response = requests.get(FRONTEND_URL, timeout=10)
        if response.status_code == 200:
            print("✅ Frontend accessible")
            return True
        else:
            print(f"❌ Frontend not accessible - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend access failed: {e}")
        return False

def create_test_resume():
    """Create a test resume file"""
    test_resume_content = """
John Doe
Software Engineer
Email: john.doe@email.com
Phone: (555) 123-4567

SKILLS:
- Python
- JavaScript
- React
- SQL
- Git
- Docker
- AWS
- Machine Learning

EXPERIENCE:
Software Developer | Tech Corp | 2020-2023
- Developed web applications using React and Node.js
- Built REST APIs with Python and FastAPI
- Worked with PostgreSQL databases
- Deployed applications on AWS
- Collaborated with cross-functional teams

Junior Developer | StartupXYZ | 2018-2020
- Created responsive web interfaces
- Implemented user authentication systems
- Optimized database queries for performance

EDUCATION:
Bachelor of Computer Science | University of Technology | 2014-2018
- Relevant coursework: Data Structures, Algorithms, Database Systems
- GPA: 3.7/4.0

PROJECTS:
E-commerce Platform
- Built full-stack web application with React and Python
- Integrated payment processing and user management
- Deployed using Docker containers

Data Analysis Tool
- Created Python scripts for data processing
- Used Pandas and NumPy for statistical analysis
- Visualized results with Matplotlib
"""
    
    with open("test_resume.txt", "w") as f:
        f.write(test_resume_content)
    
    return "test_resume.txt"

def test_file_upload():
    """Test file upload functionality"""
    print("🔍 Testing file upload...")
    
    # Create test file
    test_file = create_test_resume()
    
    try:
        with open(test_file, "rb") as f:
            files = {"file": (test_file, f, "text/plain")}
            response = requests.post(f"{BASE_URL}/upload_resume", files=files, timeout=15)
        
        # Clean up
        os.remove(test_file)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                file_id = data.get('file_id')
                print(f"✅ File upload successful - File ID: {file_id[:8]}...")
                return file_id
            else:
                print(f"❌ Upload failed: {data.get('message')}")
                return None
        else:
            print(f"❌ Upload failed - Status: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Upload test failed: {e}")
        # Clean up on error
        if os.path.exists(test_file):
            os.remove(test_file)
        return None

def test_resume_analysis(file_id):
    """Test resume analysis functionality"""
    print("🔍 Testing resume analysis...")
    
    job_description = """
We are looking for a Senior Software Engineer with expertise in:
- Python programming and web frameworks
- React and modern JavaScript
- Cloud platforms (AWS, Azure)
- Database design and optimization
- Machine learning and data analysis
- Docker containerization
- Agile development methodologies

Requirements:
- 3+ years of software development experience
- Strong problem-solving skills
- Experience with REST API development
- Knowledge of CI/CD pipelines
- Excellent communication skills
"""
    
    try:
        data = {
            "file_id": file_id,
            "job_description": job_description
        }
        
        response = requests.post(f"{BASE_URL}/analyze_resume", data=data, timeout=20)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                analysis = result.get('analysis', {})
                print(f"✅ Analysis successful:")
                print(f"   • Fit Score: {analysis.get('fit_score')}%")
                print(f"   • Selection Probability: {analysis.get('selection_probability')}%")
                print(f"   • Matched Skills: {len(analysis.get('matched_skills', []))}")
                print(f"   • Missing Skills: {len(analysis.get('missing_skills', []))}")
                print(f"   • Feedback Items: {len(analysis.get('feedback', []))}")
                return True
            else:
                print(f"❌ Analysis failed: {result.get('message')}")
                return False
        else:
            print(f"❌ Analysis failed - Status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Analysis test failed: {e}")
        return False

def test_job_matching(file_id):
    """Test job matching functionality"""
    print("🔍 Testing job matching...")
    
    try:
        response = requests.get(f"{BASE_URL}/match_jobs", params={"file_id": file_id}, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                matches = result.get('matches', [])
                print(f"✅ Job matching successful:")
                print(f"   • Total Matches: {len(matches)}")
                
                if matches:
                    top_match = matches[0]
                    print(f"   • Top Match: {top_match.get('role_title')} at {top_match.get('company')}")
                    print(f"   • Fit Score: {top_match.get('fit_score')}%")
                    print(f"   • Selection Probability: {top_match.get('selection_probability')}%")
                
                return True
            else:
                print(f"❌ Job matching failed: {result.get('message')}")
                return False
        else:
            print(f"❌ Job matching failed - Status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Job matching test failed: {e}")
        return False

def test_demo_endpoint():
    """Test demo data endpoint"""
    print("🔍 Testing demo endpoint...")
    
    try:
        response = requests.get(f"{BASE_URL}/demo_data", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            sample_analysis = data.get('sample_analysis', {})
            sample_jobs = data.get('sample_jobs', [])
            
            print(f"✅ Demo endpoint working:")
            print(f"   • Sample fit score: {sample_analysis.get('fit_score')}%")
            print(f"   • Sample jobs: {len(sample_jobs)}")
            return True
        else:
            print(f"❌ Demo endpoint failed - Status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Demo endpoint test failed: {e}")
        return False

def run_complete_test():
    """Run complete application test suite"""
    print("🧪 AI RESUME ANALYZER - COMPLETE TEST SUITE")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 6
    
    # Test 1: Backend Health
    if test_backend_health():
        tests_passed += 1
    
    # Test 2: Frontend Access
    if test_frontend_access():
        tests_passed += 1
    
    # Test 3: Demo Endpoint
    if test_demo_endpoint():
        tests_passed += 1
    
    # Test 4: File Upload
    file_id = test_file_upload()
    if file_id:
        tests_passed += 1
        
        # Test 5: Resume Analysis (depends on upload)
        if test_resume_analysis(file_id):
            tests_passed += 1
        
        # Test 6: Job Matching (depends on upload)
        if test_job_matching(file_id):
            tests_passed += 1
    
    # Results
    print("\n" + "=" * 50)
    print(f"📊 TEST RESULTS: {tests_passed}/{total_tests} PASSED")
    print("=" * 50)
    
    if tests_passed == total_tests:
        print("🎉 ALL TESTS PASSED! Your application is working perfectly.")
        print("\n✅ READY FOR PRODUCTION:")
        print("   • Backend API is fully functional")
        print("   • Frontend is accessible")
        print("   • File upload works correctly")
        print("   • Resume analysis is operational")
        print("   • Job matching is working")
        print("   • All endpoints are responsive")
    else:
        print(f"⚠️  {total_tests - tests_passed} tests failed. Check the logs above.")
        print("\n🔧 TROUBLESHOOTING:")
        print("   • Ensure both backend and frontend are running")
        print("   • Check that ports 9000 and 5173 are available")
        print("   • Verify all dependencies are installed")
        print("   • Review server logs for errors")
    
    print(f"\n🌐 Access your application at:")
    print(f"   • Frontend: {FRONTEND_URL}")
    print(f"   • Backend:  {BASE_URL}")
    print(f"   • API Docs: {BASE_URL}/docs")

if __name__ == "__main__":
    print("⏳ Waiting 5 seconds for servers to start...")
    time.sleep(5)
    run_complete_test()
