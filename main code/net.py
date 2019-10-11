from lcd import *
import requests
import json

upload_url = 'http://192.168.0.3:8000/api/data_upload'
download_url = 'http://localhost:8000/ajax/all_list_Schedule'
test_url='https://www.google.com.tw/webhp?hl=zh-TW'

params1 = "E111585004FCC6224266200240005400"
params2 = "P111585004FCC6224266206D1CDF2B0988700000"

def net_initializing():
    #check django Server Satute
    global test_url
    lcd_clearall()
    lcd_print(0,0,0.5,"Net Initializing")
    lcd_print(1,0,2,"Connecting.....    ")
    try:
        response = requests.get(test_url,timeout=20)
        response.raise_for_status()
        lcd_print(1,0,1,"SUCCESS!        ")
        return True
    except requests.exceptions.RequestException as e:
        lcd_print(1,0,1,"FAIL!          ")
        return False
    finally:
        lcd_clearall()

def upload_data(url,text):
    try:
        params = {'DATA': text}
        headers = {'content-type': 'application/json'}
        response = requests.post(url, data=json.dumps(params), headers=headers,timeout=20)
        response.raise_for_status()
        return True
        #print(response.text)
    except requests.exceptions.RequestException as e:
        return False

def download_schedule(url,text):
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
    a=upload_data(upload_url,params2)
    print(a)
