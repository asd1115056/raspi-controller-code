import json
import requests
url = "http://localhost:8000/json_upload"
params = {'Tag':'KFJM142','water_drink':112,'food_eat':1132,'active_time':'2019-09-23 11:56:00'} 
headers = {'content-type': 'application/json'}
response = requests.post(url,data=json.dumps(params),headers=headers)
print(response)
#print(response.text)