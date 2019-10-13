from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from ble import *
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


def BT_sync(command):
    global upload_url
    sucess = 0
    fail = 0
    lcd_clearall()
    lcd_print(0,0,1,"Sync begining")
    print("Load Device'mac from file")
    try:
        with open('device_list.txt', 'r') as f:
            device_mac_list = eval(f.readline())
        for mac in device_mac_list:
            print(mac)
            if command=="env":
                temp = ble(mac,"upe")
                #print(temp)
                if temp!="":
                    if temp !="Timedout!":
                        f = open("env.txt", 'w')
                        print(temp, file=f)
                        f.close()
                        time.sleep(5) #等待藍芽斷線
                        temp = ble(mac,"dle")
                        print(temp)
                        if temp == "Del:ok":
                            print("Sucess Del Arduino's env.txt")
                        else:
                            print("Error")
                        print("Upload begining")
                        f = open("env.txt")
                        while True:
                            line = f.readline()
                            if len(line) == 35: #簡單的資料長度驗證
                                if upload_data(upload_url,line):
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
                            print("Sucess Del Pi's env.txt")
                        else:
                            print("The file does not exist")
                        lcd_print(1,0,1,"Done!             ")
                    else:
                        lcd_print(1,0,1,"Timed out!            ")
                else:
                    lcd_print(1,0,1,"Fail!,No data")
                    time.sleep(5)
            if command=="pet":
                temp = ble(mac,"upp")
                #print(temp)
                if temp!="":
                    if temp !="Timedout!":
                        f = open("pet.txt", 'w')
                        print(temp, file=f)
                        f.close()
                        time.sleep(10) #等待藍芽斷線
                        temp = ble(mac,"dlp")
                        print(temp)
                        if temp == "Del:ok":
                            print("Sucess Del Arduino's pet.txt")
                        else:
                            print("Error")
                        print("Upload begining")
                        f = open("pet.txt")
                        while True:
                            line = f.readline()
                            if len(line) == 35: #簡單的資料長度驗證
                                if upload_data(upload_url,line):
                                    sucess += 1
                                else:
                                    fail += 1
                            else:
                                break
                            time.sleep(0.1)
                        print("Sucess: " + str(sucess) + " Fail: " + str(fail))
                        f.close()
                        if os.path.exists("pet.txt"):
                            os.remove("prt.txt")
                            print("Sucess Del Pi's pet.txt")
                        else:
                            print("The file does not exist")
                        lcd_print(1,0,1,"Done!             ")
                    else:
                        lcd_print(1,0,1,"Timed out!            ")
                else:
                    lcd_print(1,0,1,"Fail!,No data")
                    time.sleep(10)
    except IOError:
        print("Error: file no find or can not read")

def Schedule_sync():
    global sched,schedule_list_url,device_list_url
    #開機時網路測試順便刪掉暫存檔
    schedule_list=download_schedule(schedule_list_url)
    if  schedule_list:
        try:
            with open('schedule.txt', 'r') as f:
                file_data = f.readline()
                if  file_data:
                    if  eval(schedule_list)==eval(file_data):
                        print(sched.get_jobs(),"Schedule_list same, pass")
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

def Device_sync():
    global device_list_url
    device_list=download_device(device_list_url)
    if  device_list:
        try:
            with open('device_list.txt', 'r') as f:
                device_list_data = f.readline()
                if  device_list_data:
                    if  eval(device_list)==eval(device_list_data):
                        print("Device_list smae, pass")
                        pass
                    else:
                        #刪掉舊任務後創建新任務並存檔
                        with open('device_list.txt', 'w') as f:
                            f.write(device_list_data)
                else:
                    #直接創新的
                    print("Create new Device_list")
                    with open('device_list.txt', 'w') as f:
                        f.write(device_list_data)
        except IOError:
            #檔案可能無法讀取或不存在
            #直接創新的
            with open('device_list.txt', 'w') as f:
                f.write(device_list_data)
            print("Error: file no find or can not read")
    else:
        #沒有網路連線時
        print("Lost connect!")
        #lcd 顯示 Lost connect!
        pass




if __name__ == "__main__":
    #sync_time()
    #sched.add_job(Schedule_sync, 'interval', seconds=10)
    #sched.add_job(task1, 'interval', seconds=10)
    #sched.add_job(BT_sync_env, 'interval', seconds=60)
    #sched.add_job(BT_sync_pet, 'interval', seconds=120)
    # BT_update("env")
    #sched.start()
    Device_sync()
    BT_sync("env")