"""
Debug Frontend-Backend Data Transfer
Test the actual data flow between frontend and backend
"""

import requests
import json
from pathlib import Path

def debug_data_transfer():
    base_url = "http://localhost:9002"
    
    print("=== DEBUGGING FRONTEND-BACKEND DATA TRANSFER ===")
    print("Testing with the exact same data the frontend would send")
    
    # Test with a simple resume that should definitely work
    test_resume_content = """
John Doe
Software Engineer

SKILLS:
Python
JavaScript  
React
Machine Learning
TensorFlow
AWS
Docker
SQL
"""
    
    print(f"Test resume content:\n{test_resume_content}")
    
    # Step 1: Test upload
    print("\n1. Testing file upload...")
    test_file_path = Path("debug_resume.txt")
    with open(test_file_path, 'w') as f:
        f.write(test_resume_content)
    
    try:
        with open(test_file_path, 'rb') as f:
            files = {'file': ('debug_resume.txt', f, 'text/plain')}
            upload_response = requests.post(f"{base_url}/upload_resume", files=files)
        
        print(f"Upload Status: {upload_response.status_code}")
        upload_result = upload_response.json()
        print(f"Upload Success: {upload_result.get('success')}")
        print(f"Skills Found: {len(upload_result.get('extracted_skills', []))}")
        print(f"Extracted Skills: {upload_result.get('extracted_skills', [])}")
        
        if upload_result.get('success'):
            file_id = upload_result['file_id']
            
            # Step 2: Test analysis with simple job description
            print(f"\n2. Testing analysis with file_id: {file_id}")
            
            job_desc = "Looking for Python developer with React and Machine Learning experience"
            
            analysis_data = {
                'file_id': file_id,
                'job_description': job_desc
            }
            
            analysis_response = requests.post(f"{base_url}/analyze_resume", data=analysis_data)
            print(f"Analysis Status: {analysis_response.status_code}")
            
            if analysis_response.status_code == 200:
                analysis_result = analysis_response.json()
                print(f"Analysis Success: {analysis_result.get('success')}")
                
                if analysis_result.get('success'):
                    analysis = analysis_result['analysis']
                    print(f"\nAnalysis Results:")
                    print(f"  Fit Score: {analysis.get('fit_score', 'N/A')}%")
                    print(f"  Skill Match: {analysis.get('skill_match_score', 'N/A')}%")
                    print(f"  Matched Skills: {analysis.get('matched_skills', [])}")
                    print(f"  Missing Skills: {analysis.get('missing_skills', [])}")
                    print(f"  Total Skills Found: {analysis.get('total_skills_found', 0)}")
                else:
                    print(f"Analysis failed: {analysis_result.get('message', 'Unknown error')}")
            else:
                print(f"Analysis request failed: {analysis_response.text}")
            
            # Step 3: Test job matching
            print(f"\n3. Testing job matching...")
            matches_response = requests.get(f"{base_url}/match_jobs?file_id={file_id}")
            print(f"Matches Status: {matches_response.status_code}")
            
            if matches_response.status_code == 200:
                matches_result = matches_response.json()
                print(f"Matches Success: {matches_result.get('success')}")
                print(f"Eligible Jobs: {matches_result.get('eligible_matches', 0)}")
                print(f"Total Jobs: {matches_result.get('total_matches', 0)}")
                
                matches = matches_result.get('matches', [])
                if matches:
                    print(f"\nTop Match:")
                    top_match = matches[0]
                    print(f"  Company: {top_match.get('company')}")
                    print(f"  Role: {top_match.get('role_title')}")
                    print(f"  Fit Score: {top_match.get('fit_score')}%")
                    print(f"  Skills Overlap: {top_match.get('skills_overlap', [])}")
            else:
                print(f"Matches request failed: {matches_response.text}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if test_file_path.exists():
            test_file_path.unlink()
    
    # Step 4: Test direct skill extraction
    print(f"\n4. Testing direct skill extraction...")
    try:
        # Import the skill extraction function directly
        import sys
        sys.path.append('.')
        from fixed_enhanced_backend import extract_skills_enhanced
        
        categories, skills = extract_skills_enhanced(test_resume_content)
        print(f"Direct extraction - Skills found: {len(skills)}")
        print(f"Direct extraction - Skills: {skills}")
        print(f"Direct extraction - Categories: {list(categories.keys())}")
        
    except Exception as e:
        print(f"Direct extraction error: {e}")

if __name__ == "__main__":
    debug_data_transfer()
