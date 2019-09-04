import time
import requests

url1 = 'http://localhost:8000/ajax/all_list_Schedule'

def net_initialization():
    statue=True
    global url1
    while statue:
        try:
            response = requests.get(url1)
            response.raise_for_status()
            statue=False
        except requests.exceptions.RequestException:
            print("fail:wait for 40 sec")
            time.sleep(40)

if __name__ == "__main__":
    net_initialization()