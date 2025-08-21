import requests
import json

def test_xagent_api():
    payload = {
        "task": "Say hello world",
        "tools": [],
        "model": "gpt-3.5-turbo",
        "history": [{"role": "system", "content": "You are a helpful assistant."}]
    }
    try:
        response = requests.post("http://localhost:8090/agent/run", json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    success = test_xagent_api()
    print(f"XAgent API test {'passed' if success else 'failed'}")