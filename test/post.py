import json
import requests
url="http://localhost:8000/ajax/control_input"


while True:
    try:
        response = requests.get(url,timeout=1)
        response.raise_for_status()
        print( response.text)
    except requests.exceptions.RequestException as e:
        pass