from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
#from ble import *
#from net import *
import requests
import ntplib
import time
import os
import json

url = 'http://localhost:8000/ajax/all_list_Schedule'
sched = BlockingScheduler()
count = 0


def sync_time():
    try:
        c = ntplib.NTPClient()
        response = c.request('pool.ntp.org')
        ts = response.tx_time
        _date = time.strftime('%Y-%m-%d', time.localtime(ts))
        _time = time.strftime('%X', time.localtime(ts))
        os.system('date {} && time {}'.format(_date, _time))
    except:
        print('sync_time:could not sync with time server.')
    print('sync_time:Done.')


def Add_Scheduler(x):
    id_count = 0
    for u in x:
        temp = datetime.strptime(u['schedule_time'], '%H:%M:%S')
        sched.add_job(task, 'cron', id=str(id_count), hour=temp.hour,minute=temp.minute, kwargs={"a": u['Tag'], "b": u['food_amount']})
        id_count += 1


def delete_Scheduler(x):
    for j in range(0, x):
        sched.remove_job(str(j))


def task(a, b):
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), a, b)

def BT_sync():
    print ("BT_sync: begin")
    flag=True
    count=0
    while flag:
        env_temp=ble("upe")
        if env_temp != "":
            flag=False
        else:
            print ("BT_sync fail!"+ " Retry "+ str(count) +" time")
            time.sleep(30)
        count+=1
        if count>3:
            print ("BT_sync fail!"+ " timeout")
            break
    if count<3 and env_temp !="":
        f = open('env.txt','w')
        print(env_temp, file = f)
        f.close()
        time.sleep(5)
        env_temp=ble("dle")
        if env_temp=="Del:ok":
            print ("BT_sync: done")
def BT_update():
    count=0
    f=open("env.txt")
    while True:
        line = f.readline()
        count+=1
        if len(line)==22: 
            print(str(count)+"  "+line)
        else:
            break

def sync(url):
    global sched, count
    new = []
    try:
        response = requests.get(url)
        response.raise_for_status()
        r = json.loads(response.text)
        for di in r:
            new.append(di['fields'])
        if count == 0:
            Add_Scheduler(new)
            print(sched.get_jobs(), 'Connection:first')
            with open('Scheduler_save.txt', 'w') as f:
                f.write(str(new))
            count = 1
        else:
            with open('Scheduler_save.txt', 'r') as f:
                output = eval(f.readline())
            if new != output:
                delete_Scheduler(len(output))
                Add_Scheduler(new)
                print(sched.get_jobs(), 'Connection:change')
                with open('Scheduler_save.txt', 'w') as f:
                    f.write(str(new))
            else:
                print(sched.get_jobs(), 'Connection:same')
    except requests.exceptions.RequestException:
        try:
            with open('Scheduler_save.txt', 'r') as f:
                output = eval(f.readline())
        except IOError:
            print("Error: file no find or can not read")
        else:
            if count == 0:
                Add_Scheduler(output)
                print(sched.get_jobs(), 'ConnectionError:first')
                count = 1
            else:
                delete_Scheduler(len(output))
                Add_Scheduler(output)
                print(sched.get_jobs(), 'ConnectionError:same')


if __name__ == "__main__":
    #sync_time()
    #sched.add_job(sync, 'interval', seconds=5,args=[url])
    #sched.add_job(task1, 'interval', seconds=10)
    #sched.add_job(BT_sync, 'interval', seconds=10)
    BT_update()
    #sched.start()
    #pass
