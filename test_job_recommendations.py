import requests
import json

def test_job_recommendations():
    # First upload a resume
    upload_url = "http://localhost:9001/upload_resume"
    file_path = "resume_alice.pdf"
    
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (file_path, f, 'application/pdf')}
            upload_response = requests.post(upload_url, files=files)
            
        print(f"Upload Status: {upload_response.status_code}")
        
        if upload_response.status_code == 200:
            # Now get job recommendations
            job_url = "http://localhost:9001/job-recommendations"
            job_response = requests.get(job_url)
            
            print(f"Job Recommendations Status: {job_response.status_code}")
            
            if job_response.status_code == 200:
                data = job_response.json()
                print(f"\nCandidate: {data['candidate_name']}")
                print(f"Total Skills: {data['total_skills']}")
                print(f"Message: {data['message']}")
                print("\nJob Recommendations:")
                
                for i, job in enumerate(data['job_recommendations'][:3], 1):  # Show top 3
                    print(f"\n{i}. {job['title']} - {job['fit_score']}% Match")
                    print(f"   Salary: {job['salary_range']}")
                    print(f"   Experience: {job['experience_level']}")
                    print(f"   Description: {job['description']}")
                    if job.get('matching_skills'):
                        print(f"   Required Skills Match: {', '.join(job['matching_skills']['required'])}")
                        if job['matching_skills']['preferred']:
                            print(f"   Preferred Skills Match: {', '.join(job['matching_skills']['preferred'])}")
            else:
                print(f"Job recommendations failed: {job_response.text}")
        else:
            print(f"Upload failed: {upload_response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_job_recommendations()
