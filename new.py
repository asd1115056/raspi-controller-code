from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import requests
import json
import os 
import time 
import ntplib 

url1 = 'http://localhost:8000/ajax/all_list_Schedule'
sched = BlockingScheduler()
count=0

def sync_time():
    try:  
        c = ntplib.NTPClient() 
        response = c.request('pool.ntp.org') 
        ts = response.tx_time 
        _date = time.strftime('%Y-%m-%d',time.localtime(ts)) 
        _time = time.strftime('%X',time.localtime(ts)) 
        os.system('date {} && time {}'.format(_date,_time)) 
    except:
        print('sync_time:could not sync with time server.')
    print('sync_time:Done.')

def Add_Scheduler(x):
    id_count=0
    for u in x:
        temp = datetime.strptime(u['schedule_time'], '%H:%M:%S')
        sched.add_job(task, 'cron',id=str(id_count), hour=temp.hour, minute=temp.minute, kwargs={"a": u['Tag'], "b": u['food_amount']})
        id_count+=1

def delete_Scheduler(x):
    for j in range(0 ,x):
        sched.remove_job(str(j))

def task(a, b):
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), a, b)


def sync():  
    global url1,sched,count
    new = []
    try:
        response = requests.get(url1)
        response.raise_for_status()
        r=json.loads(response.text)
        for di in r:
            new.append(di['fields'])
        if count==0:
            Add_Scheduler(new)
            print(sched.get_jobs(), 'Connection:first')
            with open('Scheduler_save.text', 'w') as f:
                f.write(str(new))
            count = 1
        else:
            with open('Scheduler_save.text', 'r') as f:
                output = eval(f.readline())
            if new != output:
                delete_Scheduler(len(output))
                Add_Scheduler(new)
                print(sched.get_jobs(), 'Connection:change')
                with open('Scheduler_save.text', 'w') as f:
                    f.write(str(new))
            else:
                print(sched.get_jobs(), 'Connection:same')  
    except requests.exceptions.RequestException:
        try:
            with open('Scheduler_save.text', 'r') as f:
                output = eval(f.readline())
        except IOError:
            print("Error: 没有找到文件或读取文件失败(ConnectionError)")
        else:
            if count==0:
                Add_Scheduler(output)
                print(sched.get_jobs(), 'ConnectionError:first')
                count = 1
            else:
                delete_Scheduler(len(output))
                Add_Scheduler(output)
                print(sched.get_jobs(), 'ConnectionError:same')

if __name__ == "__main__":
    sync_time()
    sched.add_job(sync, 'interval', seconds=5)
    sched.start()
