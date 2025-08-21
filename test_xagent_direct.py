import requests
import json

def test_xagent_completion():
    """
    Tests the most common API endpoint for agent systems.
    """
    url = "http://localhost:8090/v1/chat/completions"
    
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": "Hello, can you say hello world?"}],
        "stream": False
    }
    
    headers = {
        "Content-Type": "application/json",
        # Try with and without authorization
        "Authorization": "Bearer xagent" 
    }
    
    try:
        print(f"Testing endpoint: {url}")
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ SUCCESS: XAgent is working correctly!")
            result = response.json()
            print("Agent response:", result['choices'][0]['message']['content'])
            return True
        else:
            print("❌ Endpoint not found or error occurred.")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

if __name__ == "__main__":
    test_xagent_completion()