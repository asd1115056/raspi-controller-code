from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import requests
import json
import logging

url1 = 'http://localhost:8000/ajax/all_list_Schedule'
sched = BlockingScheduler()


def Add_Scheduler(x):
    sched.remove_all_jobs()
    for u in x:
        temp = datetime.strptime(u['schedule_time'], '%H:%M:%S')
        sched.add_job(task, 'cron', hour=temp.hour, minute=temp.minute, kwargs={"a": u['Tag'], "b": u['food_amount']})


def task(a, b):
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), a, b)


def sync():
    global url1, sched
    try:
        r = requests.get(url1)
    except requests.exceptions.RequestException:
        try:
            with open('Scheduler_save.text', 'r') as f:
                output = eval(f.readline())
        except IOError:
            print("Error: 没有找到文件或读取文件失败(ConnectionError)")
        else:
            Add_Scheduler(output)
            print(sched.get_jobs(), 'ConnectionError')
    else:
        if r.status_code == 200:
            temp1 = []
            r = json.loads(r.text)
            for di in r:
                temp1.append(di['fields'])
            try:
                with open('Scheduler_save.text', 'r') as f:
                    output = eval(f.readline())
            except IOError:
                print("Error: 没有找到文件或读取文件失败(200)")
                Add_Scheduler(temp1)
                print(sched.get_jobs(), 'first')
                with open('Scheduler_save.text', 'w') as f:
                    f.write(str(temp1))
            else:
                if temp1 != output:
                    Add_Scheduler(temp1)
                    print(sched.get_jobs(), 'check')
                    with open('Scheduler_save.text', 'w') as f:
                        f.write(str(temp1))
                else:
                    None
        else:
            print("reconnect")
            try:
                with open('Scheduler_save.text', 'r') as f:
                    output = eval(f.readline())
            except IOError:
                print("Error: 没有找到文件或读取文件失败")
            else:
                Add_Scheduler(output)
                print(sched.get_jobs(), 'reconnect')


sched.add_job(sync, 'interval', seconds=10)
sched.start()
