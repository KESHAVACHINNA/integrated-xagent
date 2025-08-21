import requests
import json

def test_endpoint(url, method="GET", data=None, auth=True):
    headers = {"Content-Type": "application/json"}
    if auth:
        headers["Authorization"] = "Bearer xagent"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        else:
            response = requests.post(url, json=data, headers=headers, timeout=10)
        
        print(f"Testing: {url}")
        print(f"Status: {response.status_code}")
        if response.status_code < 400:
            print(f"Response: {response.text}")
            if "application/json" in response.headers.get("Content-Type", ""):
                try:
                    json_response = response.json()
                    print("JSON Response:", json.dumps(json_response, indent=2))
                except:
                    pass
            return True
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {e}")
    
    print("---")
    return False

# Test various endpoints
endpoints = [
    # Common API patterns
    ("http://localhost:8090/api/chat", "POST", {"message": "Hello"}),
    ("http://localhost:8090/v1/chat/completions", "POST", 
     {"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "Hello"}]}),
    ("http://localhost:8090/chat", "POST", {"message": "Hello"}),
    
    # Health/status endpoints
    ("http://localhost:8090/health", "GET"),
    ("http://localhost:8090/status", "GET"),
    ("http://localhost:8090/api/health", "GET"),
    
    # Info endpoints
    ("http://localhost:8090/info", "GET"),
    ("http://localhost:8090/api/info", "GET"),
    
    # Try without authentication
    ("http://localhost:8090/", "GET", None, False),
    ("http://localhost:8090/api", "GET", None, False),
]

print("Testing XAgent API endpoints...")
print("=" * 50)

found_working = False
for endpoint in endpoints:
    url = endpoint[0]
    method = endpoint[1]
    data = endpoint[2] if len(endpoint) > 2 else None
    auth = endpoint[3] if len(endpoint) > 3 else True
    
    if test_endpoint(url, method, data, auth):
        found_working = True
        print(f"✅ Found working endpoint: {url}")
        break

if not found_working:
    print("❌ No working endpoints found. Please check:")
    print("1. The XAgent server is running (docker ps shows containers)")
    print("2. Try accessing the web interface at http://localhost:5173")
    print("3. Check XAgent documentation for correct API endpoints")