from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
#from ble import *
from net import *
import requests
import ntplib
import time
import os
import json


url = 'http://localhost:8000/ajax/all_list_Schedule'
data_upload = "http://localhost:8000/api/data_upload"
sched = BlockingScheduler()
count = 0

def Add_Scheduler(x):
    id_count = 0
    for u in x:
        temp = datetime.strptime(u['schedule_time'], '%H:%M:%S')
        sched.add_job(task, 'cron', id=str(id_count), hour=temp.hour,minute=temp.minute, kwargs={"a": u['mac'],"b": u['Tag'], "c": u['food_amount']})
        id_count += 1


def Delete_Scheduler(x):
    for j in range(0, x):
        sched.remove_job(str(j))


def task(a, b, c):
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), a, b, c )


def BT_sync_env():
    #lcd_clearall()
    #lcd_print(1,0,1"Sync begining")
    pass
'''
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
'''


def Schedule_sync():
    global sched,schedule_list_url,device_list_url
    #開機時網路測試順便刪掉暫存檔
    schedule_list=download_schedule(schedule_list_url)
    device_list=download_device(device_list_url)
    if  device_list:
        try:
            with open('schedule.txt', 'r') as f:
                file_data = f.readline()
                if  file_data:
                    if  eval(device_list)==eval(file_data):
                        print("Same data pass")
                        pass
                    else:
                        #刪掉舊任務後創建新任務並存檔
                        Add_Scheduler(eval(device_list))
                        with open('schedule.txt', 'w') as f:
                            f.write(device_list)
                else:
                    #直接創新的
                    print("Create new Scheduler")
                    with open('schedule.txt', 'w') as f:
                        f.write(device_list)
        except IOError:
            #檔案可能無法讀取或不存在
            #直接創新的
            with open('schedule.txt', 'w') as f:
                f.write(device_list)
            print("Error: file no find or can not read")
    else:
        #沒有網路連線時
        print("Lost connect!")
        #lcd 顯示 Lost connect!
        pass

    if  schedule_list:
        try:
            with open('schedule.txt', 'r') as f:
                file_data = f.readline()
                if  file_data:
                    if  eval(schedule_list)==eval(file_data):
                        print(sched.get_jobs(),"Same data pass")
                        pass
                    else:
                        #刪掉舊任務後創建新任務並存檔
                        print("Del old Scheduler")
                        Delete_Scheduler(len(eval(file_data)))
                        print("Create new Scheduler")
                        Add_Scheduler(eval(schedule_list))
                        with open('schedule.txt', 'w') as f:
                            f.write(schedule_list)
                else:
                    #直接創新的
                    Add_Scheduler(eval(schedule_list))
                    print("Create new Scheduler")
                    with open('schedule.txt', 'w') as f:
                        f.write(schedule_list)
        except IOError:
            #檔案可能無法讀取或不存在
            #直接創新的
            Add_Scheduler(eval(schedule_list))
            with open('schedule.txt', 'w') as f:
                f.write(schedule_list)
            print("Error: file no find or can not read")
    else:
        #沒有網路連線時
        print("Lost connect!")
        #lcd 顯示 Lost connect!
        pass



if __name__ == "__main__":
    #sync_time()
    sched.add_job(Schedule_sync, 'interval', seconds=10)
    #sched.add_job(task1, 'interval', seconds=10)
    #sched.add_job(BT_sync_env, 'interval', seconds=60)
    #sched.add_job(BT_sync_pet, 'interval', seconds=120)
    # BT_update("env")
    sched.start()
    # pass
