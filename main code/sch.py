from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
#from ble import *
#from net import *
from upload import *
import requests
import ntplib
import time
import os
import json


url = 'http://localhost:8000/ajax/all_list_Schedule'
data_upload = "http://localhost:8000/api/data_upload"
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
        sched.add_job(task, 'cron', id=str(id_count), hour=temp.hour,
                      minute=temp.minute, kwargs={"a": u['Tag'], "b": u['food_amount']})
        id_count += 1


def delete_Scheduler(x):
    for j in range(0, x):
        sched.remove_job(str(j))


def task(a, b):
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), a, b)


def BT_sync_env():
    print("BT_sync: begin")
    print("Send upe command")
    temp = ble("upe")
    if temp != "":
        print("done!")
        print("Save file....")
        f = open("env.txt", 'w')
        print(temp, file=f)
        f.close()
        print("done!")
        time.sleep(10)
        print("Send del command....")
        temp = ble("dle")
        if temp == "Del:ok":
            print("done")
        print("BT_update:begin")
        sucess = 0
        fail = 0
        f = open("env.txt")
        while True:
            line = f.readline()
            if len(line) == 22 or len(line) == 32:
                if upload(line) == 200:
                    sucess += 1
                else:
                    fail += 1
            else:
                break
        time.sleep(0.05)
        print("Sucess: " + str(sucess) + " Fail: " + str(fail))
        f.close()
        if os.path.exists("env.txt"):
            os.remove("env.txt")
            print("Sucess del env.txt")
        else:
            print("The file does not exist")
        print("done")
    else:
        print("blank")

def BT_sync_pet():
    print("BT_sync: begin")
    print("Send pet command")
    temp = ble("upp")
    if temp != "":
        print("done!")
        print("Save file....")
        f = open("pet.txt", 'w')
        print(temp, file=f)
        f.close()
        print("done!")
        time.sleep(10)
        print("Send del command....")
        temp = ble("dlp")
        if temp == "Del:ok":
            print("done")
        print("BT_update:begin")
        sucess = 0
        fail = 0
        f = open("pet.txt")
        while True:
            line = f.readline()
            if len(line) == 22 or len(line) == 32:
                if upload(line) == 200:
                    sucess += 1
                else:
                    fail += 1
            else:
                break
            time.sleep(0.05)
        print("Sucess: " + str(sucess) + " Fail: " + str(fail))
        f.close()
        if os.path.exists("pet.txt"):
            os.remove("pet.txt")
            print("Sucess del pet.txt")
        else:
            print("The file does not exist")
        print("done")
    else:
        print("blank")


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
    # sync_time()
    #sched.add_job(sync, 'interval', seconds=5,args=[url])
    #sched.add_job(task1, 'interval', seconds=10)
    sched.add_job(BT_sync_env, 'interval', seconds=60)
    sched.add_job(BT_sync_pet, 'interval', seconds=120)
    # BT_update("env")
    sched.start()
    # pass
