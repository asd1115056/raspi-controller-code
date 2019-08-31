from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import requests
import json
import logging

url1 = 'http://localhost:8000/ajax/all_list_Schedule'
sched = BlockingScheduler()

def task(a,b):
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),a,b)
def sync():
    global url1,sched
    r = requests.get(url1)
    if r.status_code == 200:
        temp1 = []
        r = json.loads(r.text)
        for di in r:
            temp1.append(di['fields'])
        try:
            with open('Scheduler_save.json','r') as f:
                output=f.read()
                output=list(output)
        except IOError:
            print ("Error: 没有找到文件或读取文件失败(200)")
            for u in temp1:
                    temp2 = datetime.strptime(u['schedule_time'], '%H:%M:%S')
                    sched.add_job(task, 'cron', hour=temp2.hour, minute=temp2.minute, kwargs={"a": u['Tag'], "b": u['food_amount']})
            print(sched.get_jobs()) 
            with open('Scheduler_save.text','w') as f:
                f.write(str(temp1)) 
        else:          
            if temp1!=output:
                sched.remove_all_jobs()
                for u in temp1:
                    temp2 = datetime.strptime(u['schedule_time'], '%H:%M:%S')
                    sched.add_job(task, 'cron', hour=temp2.hour, minute=temp2.minute, kwargs={"a": u['Tag'], "b": u['food_amount']})
                print(sched.get_jobs()) 
                with open('Scheduler_save.text','w') as f:
                    f.write(str(temp1)) 
            else:
                None      
    else:
        print("reconnect")
        try:
            with open('Scheduler_save.json','r') as f:
                output=f.read()
        except IOError:
            print ("Error: 没有找到文件或读取文件失败")
        else:          
            sched.remove_all_jobs()
            for u in output:
                temp3 = datetime.strptime(u['schedule_time'], '%H:%M:%S')
                sched.add_job(task, 'cron', hour=temp3.hour, minute=temp3.minute, kwargs={"a": u['Tag'], "b": u['food_amount']})
            print(sched.get_jobs())


sched.add_job(sync, 'interval', seconds=10)
sched.start()
