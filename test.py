from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import requests
import json
import logging

url1='http://localhost:8000/ajax/all_list_Schedule'
sched = BlockingScheduler()

#new=[{'Tag': 'EAVBR1', 'food_Name': 'tamto', 'schedule_time': '06:30:00', 'food_amount': '30.00'}, {'Tag': 'FDLMCW', 'food_Name': 'tamto', 'schedule_time': '08:00:00', 'food_amount': '50.00'}, {'Tag': 'EAVBR1', 'food_Name': 'tamto', 'schedule_time': '09:00:00', 'food_amount': '50.00'}, {'Tag': 'EAVBR1', 'food_Name': 'tamto', 'schedule_time': '12:00:00', 'food_amount': '50.00'}, {'Tag': 'FDLMCW', 'food_Name': 'tamto', 'schedule_time': '12:00:00', 'food_amount': '50.00'}]

def write_file(x):
	with open('Scheduler_save.txt','w') as f:
		f.write(x)

def read_file():
	with open('Scheduler_save.txt','r') as f:
		return f.read()

def Get_Scheduler():
	temp=[]
	r = requests.get(url1)
	r=json.loads(r.text)
	for di in r:
		#print (di['fields']) 
		temp.append( di['fields'] )
	#print (json.dumps(temp))  	
	return temp	

def Sync_Scheduler():
	sched.add_job(task, 'interval',seconds=300)

def task(a,b):
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),a,b)

def Create_Scheduler(x):
	global i
	i=0
	for u in x:
		temp=datetime.strptime(u['schedule_time'], '%H:%M:%S')
		#format = '%H:%M:%S'
		sched.add_job(task, 'cron',hour=temp.hour,minute=temp.minute,id=str(i),kwargs={"a":u['Tag'],"b":u['food_amount']})
		i+=1

def delete_Create_Scheduler():
	for j in i:
		sched.remove_job(str(j))






if __name__ == "__main__":
	x=Get_Scheduler()
	Create_Scheduler(x)
	print (sched.get_jobs())
	sched.start()

