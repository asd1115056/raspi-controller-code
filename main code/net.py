#from lcd import *
import requests
import json

schedule_list_url = 'http://localhost:8000/api/schedule_list'
device_list_url = 'http://localhost:8000/api/device_list'
upload_url='http://localhost:8000/api/data_upload'

test_url='https://www.google.com.tw/webhp?hl=zh-TW'

params1 = "E111585004FCC6224266200240005400"
params2 = "P111585004FCC6224266206D1CDF2B0988700000"
'''
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
        if os.path.exists("schedule.txt"):
            #刪掉暫存檔
            os.remove("schedule.txt")
            print("Remove old schedule.txt ")
        lcd_clearall()
'''

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

def download_schedule(url):
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
    a=download_schedule(schedule_list_url)
    print(a)
