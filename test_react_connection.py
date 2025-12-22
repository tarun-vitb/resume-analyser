"""
Test React Frontend Connection to Backend
Verify that the React app can receive skills data
"""

import requests
import json
from pathlib import Path

def test_react_connection():
    base_url = "http://localhost:9002"
    
    print("="*60)
    print("TESTING REACT FRONTEND CONNECTION")
    print("="*60)
    print("Verifying backend responds correctly for React app...")
    
    # Test 1: Health check
    print("\n1. Testing backend health...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("   ✓ Backend is healthy")
        else:
            print(f"   ✗ Backend health check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"   ✗ Cannot connect to backend: {e}")
        print("   Make sure the backend is running: python fixed_enhanced_backend.py")
        return
    
    # Test 2: Upload resume and check response format
    print("\n2. Testing resume upload response format...")
    
    test_resume = """
JOHN DOE
Software Developer

SKILLS:
Python, JavaScript, React, Node.js, SQL, Git
Machine Learning, TensorFlow, AWS, Docker
"""
    
    test_file_path = Path("test_react_resume.txt")
    
    try:
        with open(test_file_path, 'w') as f:
            f.write(test_resume)
        
        with open(test_file_path, 'rb') as f:
            files = {'file': ('test_react_resume.txt', f, 'text/plain')}
            response = requests.post(f"{base_url}/upload_resume", files=files)
        
        print(f"   Upload Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("   ✓ Upload successful")
            
            # Check response structure for React
            required_fields = ['success', 'file_id', 'extracted_skills']
            missing_fields = []
            
            for field in required_fields:
                if field not in result:
                    missing_fields.append(field)
            
            if missing_fields:
                print(f"   ✗ Missing required fields: {missing_fields}")
            else:
                print("   ✓ All required fields present")
                
                # Check extracted_skills specifically
                extracted_skills = result.get('extracted_skills', [])
                print(f"   📊 Skills extracted: {len(extracted_skills)}")
                print(f"   🔍 Skills found: {extracted_skills}")
                
                if len(extracted_skills) > 0:
                    print("   ✓ Skills extraction working correctly")
                    print(f"   📋 Sample skills: {extracted_skills[:5]}")
                else:
                    print("   ✗ No skills extracted - this is the problem!")
                
                # Test analysis
                print("\n3. Testing analysis response format...")
                
                job_desc = "Looking for Python developer with React and Machine Learning skills"
                
                analysis_data = {
                    'file_id': result['file_id'],
                    'job_description': job_desc
                }
                
                analysis_response = requests.post(f"{base_url}/analyze_resume", data=analysis_data)
                print(f"   Analysis Status: {analysis_response.status_code}")
                
                if analysis_response.status_code == 200:
                    analysis_result = analysis_response.json()
                    if analysis_result.get('success'):
                        analysis = analysis_result['analysis']
                        print("   ✓ Analysis successful")
                        print(f"   📊 Fit Score: {analysis.get('fit_score', 'N/A')}%")
                        print(f"   🎯 Skill Match: {analysis.get('skill_match_score', 'N/A')}%")
                        print(f"   ✅ Matched Skills: {analysis.get('matched_skills', [])}")
                    else:
                        print("   ✗ Analysis failed")
                else:
                    print(f"   ✗ Analysis request failed: {analysis_response.status_code}")
        else:
            print(f"   ✗ Upload failed: {response.status_code}")
            print(f"   Response: {response.text}")
    
    except Exception as e:
        print(f"   ✗ Test error: {e}")
    
    finally:
        if test_file_path.exists():
            test_file_path.unlink()
    
    print("\n" + "="*60)
    print("CONNECTION TEST COMPLETED")
    print("="*60)
    print("NEXT STEPS:")
    print("1. Start the backend: python fixed_enhanced_backend.py")
    print("2. Start the React frontend: python start_react_app.py")
    print("3. Open http://localhost:5173 in your browser")
    print("4. Upload a resume and check if skills are shown")

if __name__ == "__main__":
    test_react_connection()
