import json
import requests
url = "http://localhost:8000/json_upload"
params = {'Tag':'KFJM142','water_drink':1512,'food_eat':132} 
headers = {'content-type': 'application/json'}
response = requests.post(url,data=json.dumps(params),headers=headers)
print(response)
#print(response.text)