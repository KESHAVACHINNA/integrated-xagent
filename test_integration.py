import requests

def test_xagent_connection():
    """Test if we can connect to XAgent API"""
    try:
        response = requests.get("http://localhost:8090/", timeout=5)
        print(f"XAgent server status: {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"XAgent connection failed: {e}")
        return False

if __name__ == "__main__":
    if test_xagent_connection():
        print("✓ XAgent server is accessible")
    else:
        print("✗ Cannot connect to XAgent server")