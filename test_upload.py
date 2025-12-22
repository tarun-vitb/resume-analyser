import requests
import os

# Test the upload endpoint
def test_upload():
    url = "http://localhost:9001/upload_resume"
    
    # Use one of the sample resumes
    file_path = "resume_alice.pdf"
    
    if not os.path.exists(file_path):
        print(f"File {file_path} not found")
        return
    
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (file_path, f, 'application/pdf')}
            response = requests.post(url, files=files)
            
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_upload()
