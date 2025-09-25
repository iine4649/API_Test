import requests

# Use requests package to call your api address http://127.0.0.1:5000/api/joke to display a funny joke
response = requests.get("http://127.0.0.1:5000/api/joke")
if response.status_code == 200:
    data = response.json()
    print("Shun:", data.get("setup", ""), data.get("punchline", ""))
else:
    print("Failed to get a joke. Status code:", response.status_code)