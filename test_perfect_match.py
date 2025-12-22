import requests
import json

def test_perfect_match():
    """Test scoring when candidate has all required skills (0 missing skills)"""
    
    # Create a test resume with skills that perfectly match a job
    # Let's create a resume with Python, Java, JavaScript, SQL, REST API skills
    test_resume_data = {
        'name': 'Perfect Candidate',
        'skills': ['Python', 'Java', 'JavaScript', 'SQL', 'REST API', 'Flask', 'Machine Learning']
    }
    
    # Simulate uploading this data by directly calling the company matches endpoint
    # First, let's upload a resume with these exact skills
    upload_url = "http://localhost:9001/upload_resume"
    
    # Create a simple text file with these skills mentioned
    test_content = """
    Perfect Candidate
    Software Engineer
    
    Skills: Python, Java, JavaScript, SQL, REST API, Flask, Machine Learning, Data Analysis
    
    Experience:
    - Developed web applications using Python and Flask
    - Built REST APIs with Java and Spring
    - Created data analysis tools with SQL
    - Implemented machine learning models
    """
    
    # Write to a temporary file
    with open('test_perfect_resume.txt', 'w') as f:
        f.write(test_content)
    
    try:
        # Upload the test resume
        with open('test_perfect_resume.txt', 'rb') as f:
            files = {'file': ('test_perfect_resume.txt', f, 'text/plain')}
            upload_response = requests.post(upload_url, files=files)
        
        print(f"Upload Status: {upload_response.status_code}")
        if upload_response.status_code == 200:
            upload_data = upload_response.json()
            print(f"Extracted Skills: {upload_data.get('skills', [])}")
            
            # Now get company matches
            matches_url = "http://localhost:9001/company-matches"
            matches_response = requests.get(matches_url)
            
            if matches_response.status_code == 200:
                data = matches_response.json()
                print(f"\nTotal Matches: {data['total_matches']}")
                
                # Look for jobs where missing skills = 0
                perfect_matches = []
                for match in data['matches']:
                    if len(match['missing_skills']) == 0:
                        perfect_matches.append(match)
                
                print(f"\nPerfect Matches (0 missing skills): {len(perfect_matches)}")
                
                for i, match in enumerate(perfect_matches[:3], 1):
                    print(f"\n{i}. {match['role_title']} at {match['company']}")
                    print(f"   Fit Score: {match['fit_score']}%")
                    print(f"   Selection Probability: {match['selection_probability']}%")
                    print(f"   Missing Skills: {len(match['missing_skills'])} (should be 0)")
                    print(f"   Required Skills Match: {match['required_skills_match']}")
                    print(f"   Skills Overlap: {len(match['skills_overlap'])} skills")
                
                # Also show some partial matches for comparison
                partial_matches = [m for m in data['matches'] if len(m['missing_skills']) > 0][:2]
                print(f"\nPartial Matches (for comparison):")
                for i, match in enumerate(partial_matches, 1):
                    print(f"\n{i}. {match['role_title']} at {match['company']}")
                    print(f"   Fit Score: {match['fit_score']}%")
                    print(f"   Selection Probability: {match['selection_probability']}%")
                    print(f"   Missing Skills: {len(match['missing_skills'])}")
                    print(f"   Required Skills Match: {match['required_skills_match']}")
                
            else:
                print(f"Matches failed: {matches_response.text}")
        else:
            print(f"Upload failed: {upload_response.text}")
            
    except Exception as e:
        print(f"Error: {e}")
    
    # Clean up
    import os
    try:
        os.remove('test_perfect_resume.txt')
    except:
        pass

if __name__ == "__main__":
    test_perfect_match()
