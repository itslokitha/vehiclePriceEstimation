import requests

response = requests.get("https://kijiji.ca")

print (response.text)