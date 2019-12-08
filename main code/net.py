from lcd import *
import requests
import json
import os

schedule_list_url = 'http://192.168.0.3:8000/api/schedule_list'
device_list_url = 'http://192.168.0.3:8000/api/device_list'
upload_url='http://192.168.0.3:8000/api/data_upload'

test_url='http://192.168.0.3:8000'

params1 = "E111585004FCC6224266200240005400"
params2 = "P111585004FCC6224266206D1CDF2B0988700000"

def net_initializing(url):
    #check django Server Satute
    global test_url
    lcd_clearall()
    lcd_print(0,0,2,"Net Initializing")
    lcd_print(1,0,2,"Connecting.....    ")
    try:
        response = requests.get(url,timeout=20)
        response.raise_for_status()
        lcd_print(1,0,2,"SUCCESS!         ")
        return True
    except requests.exceptions.RequestException as e:
        lcd_print(1,0,2,"FAIL!           ")
        return "netf"


def upload_data(url,text):
    try:
        params = {'DATA': text}
        headers = {'content-type': 'application/json'}
        response = requests.post(url, data=json.dumps(params), headers=headers,timeout=2)
        response.raise_for_status()
        return True
        #print(response.text)
    except requests.exceptions.RequestException as e:
        return False

def download_schedule(url):
    try:
        response = requests.get(url,timeout=20)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return False
        
def download_device(url):
    try:
        response = requests.get(url,timeout=20)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return False

def control(url):
    try:
        response = requests.get(url,timeout=20)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return False

        

if __name__ == "__main__":
    '''
    bool1=net_initializing(url)
    print(bool1)
    '''
    net_initializing('http://192.168.50.112:8000')