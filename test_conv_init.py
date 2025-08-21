import requests

url = "http://localhost:8090/conv/init_conv_env"

data = {
    "user_id": "Guest",
    "token": "xagent"
}

response = requests.post(url, data=data)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")