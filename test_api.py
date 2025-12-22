#!/usr/bin/env python3
"""
Simple API Test Script
Tests the AI Resume Analyzer API endpoints
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_root():
    """Test root endpoint"""
    print("\n🔍 Testing root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            print("✅ Root endpoint working")
            data = response.json()
            print(f"   Version: {data.get('version')}")
            print(f"   Status: {data.get('status')}")
            return True
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Root endpoint failed: {e}")
        return False

def test_demo():
    """Test demo endpoint"""
    print("\n🔍 Testing demo endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/demo", timeout=5)
        if response.status_code == 200:
            print("✅ Demo endpoint working")
            data = response.json()
            demo = data.get('demo_analysis', {})
            print(f"   Match %: {demo.get('match_percentage')}")
            print(f"   Skills: {demo.get('found_skills')}")
            return True
        else:
            print(f"❌ Demo endpoint failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Demo endpoint failed: {e}")
        return False

def test_upload_text():
    """Test upload with a simple text file"""
    print("\n🔍 Testing file upload...")
    
    # Create a simple test resume
    test_resume = """
    John Doe
    Software Engineer
    
    Skills: Python, JavaScript, React, SQL, Git
    
    Experience:
    - Software Developer at Tech Corp (2020-2023)
    - Built web applications using React and Node.js
    - Worked with databases and APIs
    
    Education:
    - Bachelor of Computer Science
    """
    
    try:
        # Create temporary file
        with open("test_resume.txt", "w") as f:
            f.write(test_resume)
        
        # Upload file
        with open("test_resume.txt", "rb") as f:
            files = {"file": ("test_resume.txt", f, "text/plain")}
            response = requests.post(f"{BASE_URL}/api/v1/upload-resume", files=files, timeout=10)
        
        # Clean up
        import os
        os.remove("test_resume.txt")
        
        if response.status_code == 200:
            print("✅ File upload working")
            data = response.json()
            if data.get('success'):
                print(f"   Word count: {data['data'].get('word_count')}")
                print(f"   File type: {data['data'].get('file_type')}")
                return True
            else:
                print(f"❌ Upload failed: {data.get('message')}")
                return False
        else:
            print(f"❌ Upload failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Upload test failed: {e}")
        return False

def test_analysis():
    """Test simple analysis"""
    print("\n🔍 Testing resume analysis...")
    
    test_resume = """
    Jane Smith
    Data Scientist
    
    Skills: Python, Machine Learning, SQL, Pandas, Scikit-learn
    
    Experience:
    - Data Analyst at Analytics Inc (2021-2023)
    - Built predictive models using Python
    - Analyzed large datasets with SQL
    """
    
    job_description = """
    We are looking for a Data Scientist with experience in Python, 
    machine learning, and statistical analysis. Knowledge of SQL 
    and data visualization tools is preferred.
    """
    
    try:
        # Create temporary file
        with open("test_resume.txt", "w") as f:
            f.write(test_resume)
        
        # Analyze resume
        with open("test_resume.txt", "rb") as f:
            files = {"file": ("test_resume.txt", f, "text/plain")}
            data = {"job_description": job_description}
            response = requests.post(
                f"{BASE_URL}/api/v1/analyze-resume-simple", 
                files=files, 
                data=data, 
                timeout=15
            )
        
        # Clean up
        import os
        os.remove("test_resume.txt")
        
        if response.status_code == 200:
            print("✅ Resume analysis working")
            result = response.json()
            if result.get('success'):
                analysis = result['data']
                print(f"   Match %: {analysis.get('match_percentage')}%")
                print(f"   Skills found: {analysis.get('found_skills')}")
                print(f"   Recommendations: {len(analysis.get('recommendations', []))}")
                return True
            else:
                print(f"❌ Analysis failed: {result.get('message')}")
                return False
        else:
            print(f"❌ Analysis failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Analysis test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 AI Resume Analyzer API Tests")
    print("=" * 40)
    
    print("⏳ Waiting for server to start...")
    time.sleep(2)
    
    tests = [
        ("Health Check", test_health),
        ("Root Endpoint", test_root),
        ("Demo Endpoint", test_demo),
        ("File Upload", test_upload_text),
        ("Resume Analysis", test_analysis)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
    
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! Your API is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the server logs for details.")
    
    print("\n🌐 Access your API at:")
    print(f"   • Main API: {BASE_URL}")
    print(f"   • Documentation: {BASE_URL}/docs")
    print(f"   • Health Check: {BASE_URL}/health")

if __name__ == "__main__":
    main()
