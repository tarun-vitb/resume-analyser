import requests
import os

def test_detailed_upload():
    url = "http://localhost:9001/upload_resume"
    file_path = "resume_alice.pdf"
    
    if not os.path.exists(file_path):
        print(f"File {file_path} not found")
        return
    
    try:
        print(f"File size: {os.path.getsize(file_path)} bytes")
        print(f"File exists: {os.path.exists(file_path)}")
        
        with open(file_path, 'rb') as f:
            files = {'file': (file_path, f, 'application/pdf')}
            print("Sending request...")
            response = requests.post(url, files=files, timeout=30)
            
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response: {response.text}")
        
    except requests.exceptions.Timeout:
        print("Request timed out")
    except requests.exceptions.ConnectionError:
        print("Connection error")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    test_detailed_upload()
