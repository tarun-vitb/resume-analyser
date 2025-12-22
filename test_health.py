import requests

def test_health():
    try:
        response = requests.get("http://localhost:9001/health")
        print(f"Health check - Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Health check failed: {e}")

if __name__ == "__main__":
    test_health()
