import requests
import json

def test_company_matches():
    # First upload a resume
    upload_url = "http://localhost:9001/upload_resume"
    file_path = "resume_alice.pdf"
    
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (file_path, f, 'application/pdf')}
            upload_response = requests.post(upload_url, files=files)
            
        print(f"Upload Status: {upload_response.status_code}")
        
        if upload_response.status_code == 200:
            # Now get company matches
            matches_url = "http://localhost:9001/company-matches"
            matches_response = requests.get(matches_url)
            
            print(f"Company Matches Status: {matches_response.status_code}")
            
            if matches_response.status_code == 200:
                data = matches_response.json()
                print(f"\nCandidate: {data['candidate_name']}")
                print(f"Total Skills: {data['total_skills']}")
                print(f"Total Matches: {data['total_matches']}")
                print(f"Message: {data['message']}")
                print("\nTop Company Matches:")
                
                for i, match in enumerate(data['matches'][:3], 1):  # Show top 3
                    print(f"\n{i}. {match['role_title']} at {match['company']}")
                    print(f"   Location: {match['location']}")
                    print(f"   Salary: {match['salary_range']}")
                    print(f"   Industry: {match['industry']}")
                    print(f"   Fit Score: {match['fit_score']}%")
                    print(f"   Selection Probability: {match['selection_probability']}%")
                    print(f"   Remote Friendly: {match['remote_friendly']}")
                    print(f"   Skills Match: {len(match['skills_overlap'])} skills")
                    print(f"   Missing Skills: {len(match['missing_skills'])} skills")
            else:
                print(f"Company matches failed: {matches_response.text}")
        else:
            print(f"Upload failed: {upload_response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_company_matches()
