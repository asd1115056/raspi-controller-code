from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.executors.pool import ProcessPoolExecutor
from datetime import datetime
from ble import *
from net import *
import requests
import ntplib
import time
import os
import json
from servo import *
executors = {
    'default': ProcessPoolExecutor(10)  # 最多5个进程同时执行
}


ip = '192.168.50.112'
url = 'http://'+ip+':8000/ajax/all_list_Schedule'
url1 = 'http://'+ip+':8000'
data_upload = 'http://'+ip+':8000/api/data_upload'
servo = 'http://'+ip+':8000/api/control_output'
schedule_list_url = 'http://'+ip+':8000/api/schedule_list'
device_list_url = 'http://'+ip+':8000/api/device_list'
sched = BlockingScheduler(executors=executors)
count = 0


def Add_Scheduler(x):
    id_count = 0
    for u in x:
        temp = datetime.strptime(u['schedule_time'], '%H:%M:%S')
        sched.add_job(task, 'cron', id=str(id_count), hour=temp.hour, minute=temp.minute, kwargs={
                      "mac": u['mac'], "tag": u['Tag'], "food_amount": u['food_amount']})
        id_count += 1


def Delete_Scheduler(x):
    for j in range(0, x):
        sched.remove_job(str(j))


def task(mac, tag, food_amount):
    # "job22bb336b099.90"
    lcd_clearall()
    #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), end='')
    lcd_print(0, 0, 1, "Feed Task!             ")
    lcd_print(1, 0, 1, datetime.now().strftime("%H:%M:%S")+"      ")
    lcd_print(1, 0, 1, tag+" "+food_amount+"g"+"          ")
    food_amount = "%06.2f" % float(food_amount)
    msg = "job"+tag+food_amount
    temp = ble(mac, msg)
    if temp == "ok":
        lcd_print(1, 0, 2, "Done!             ")
    else:
        lcd_print(1, 0, 2, "Error!             ")
    lcd_clearall()


def BT_sync(command):
    global data_upload
    i = 1
    sucess = 0
    fail = 0
    error = 0
    lcd_clearall()
    lcd_print(0, 0, 1, "Sync begining")
    print("Load Device'mac from file")
    try:
        with open('device_list.txt', 'r') as f:
            device_mac_list = eval(f.readline())
        for mac in device_mac_list:
            lcd_print(1, 0, 0.5, "Devices " + str(i)+"      ")
            print(mac)
            MAC = "%s%s%s%s%s%s" % (
                mac[0:2], mac[3:5], mac[6:8], mac[9:11], mac[12:14], mac[15:17])
            if command == "env":
                temp = ble(mac, "upe")
                if temp != "":
                    if temp != "Timedout!":
                        print(temp)
                        f = open("env.txt", 'w')
                        print(temp, file=f)
                        f.close()
                        time.sleep(15)  # 等待藍芽斷線
                        temp = ble(mac, "dle")
                        print(temp)
                        if temp == "Del:ok":
                            print("Sucess! Del Arduino's env.txt")
                        else:
                            print("Error! Del Arduino's env.txt")
                        print("Upload begining")
                        f = open("env.txt")
                        while True:
                            line = f.readline()
                            if len(line) == 35:  # 簡單的資料長度驗證
                                if upload_data(data_upload, line):
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
                        lcd_print(1, 0, 1, "Done!             ")
                    else:
                        lcd_print(1, 0, 1, "Timed out!            ")
                else:
                    lcd_print(1, 0, 1, "Fail!,No data")
                    time.sleep(10)
            if command == "pet":
                temp = ble(mac, "upp")
                if temp != "":
                    if temp != "Timedout!":
                        print(temp)
                        f = open("pet.txt", 'w')
                        print(temp, file=f)
                        f.close()
                        time.sleep(15)  # 等待藍芽斷線
                        temp = ble(mac, "dlp")
                        print(temp)
                        if temp == "Del:ok":
                            print("Sucess Del Arduino's pet.txt")
                        else:
                            print("Error")
                        print("Upload begining")
                        f = open("pet.txt")
                        while True:
                            line = f.readline()
                            if len(line) == 43:  # 簡單的資料長度驗證
                                if upload_data(data_upload, line):
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
                            print("Sucess Del Pi's pet.txt")
                        else:
                            print("The file does not exist")
                        lcd_print(1, 0, 1, "Done!             ")
                    else:
                        lcd_print(1, 0, 1, "Timed out!            ")
                else:
                    lcd_print(1, 0, 1, "Fail!,No data")
                    time.sleep(10)
            if command == "all":
                temp = ble(mac, "upa")
                if temp != "":
                    if temp != "Timedout!":
                        print(temp)
                        f = open("all.txt", 'w')
                        print(temp, file=f)
                        f.close()
                        time.sleep(15)  # 等待藍芽斷線
                        temp = ble(mac, "dla")
                        print(temp)
                        if temp == "Del:ok":
                            print("Sucess! Del Arduino's all.txt")
                        else:
                            print("Error! Del Arduino's all.txt")
                        print("Upload begining")
                        f = open("all.txt")
                        while True:
                            line = f.readline()
                            if len(line) == 35:  # 簡單的資料長度驗證
                                line = line[0:1]+str(MAC)+line[13:34]
                                if upload_data(data_upload, line):
                                    sucess += 1
                                else:
                                    fail += 1
                            elif len(line) == 43:
                                line = line[0:1]+str(MAC)+line[13:44]
                                if upload_data(data_upload, line):
                                    sucess += 1
                                else:
                                    fail += 1
                            else:
                                error += 1
                            if line == '':
                                break
                            time.sleep(0.001)
                        print("Sucess: " + str(sucess) + " Fail: " +
                              str(fail) + " Error: "+str(error))
                        f.close()
                        if os.path.exists("all.txt"):
                            os.remove("all.txt")
                            print("Sucess Del Pi's all.txt")
                        else:
                            print("The file does not exist")
                        lcd_print(1, 0, 1, "Done!             ")
                    else:
                        lcd_print(1, 0, 1, "Timed out!            ")
                else:
                    lcd_print(1, 0, 1, "Fail!,No data")
                    time.sleep(10)
            i += 1
    except IOError:
        print("Error: Device.txt no find or can not read")


def Schedule_sync():
    global sched, schedule_list_url
    # 開機時網路測試順便刪掉暫存檔
    schedule_list = download_schedule(schedule_list_url)
    if schedule_list:
        try:
            with open('schedule.txt', 'r') as f:
                file_data = f.readline()
                if file_data:
                    if eval(schedule_list) == eval(file_data):
                        print(sched.get_jobs(), "Schedule_list same, pass")
                        pass
                    else:
                        # 刪掉舊任務後創建新任務並存檔
                        print("Del old Scheduler")
                        Delete_Scheduler(len(eval(file_data)))
                        print("Create new Scheduler")
                        Add_Scheduler(eval(schedule_list))
                        with open('schedule.txt', 'w') as f:
                            f.write(schedule_list)
                else:
                    # 直接創新的
                    Add_Scheduler(eval(schedule_list))
                    print("Create new Scheduler")
                    with open('schedule.txt', 'w') as f:
                        f.write(schedule_list)
        except IOError:
            # 檔案可能無法讀取或不存在
            # 直接創新的
            Add_Scheduler(eval(schedule_list))
            with open('schedule.txt', 'w') as f:
                f.write(schedule_list)
            print("Error: file no find or can not read")
            print("Create new Scheduler")
    else:
        # 沒有網路連線時
        print("Lost connect!")
        # lcd 顯示 Lost connect!
        pass


def Device_sync():
    global device_list_url
    device_list = download_device(device_list_url)
    # print(device_list)
    if device_list:
        try:
            with open('device_list.txt', 'r') as f:
                file_data = f.readline()
                if file_data:
                    if eval(device_list) == eval(file_data):
                        print("Device_list smae, pass")
                        pass
                    else:
                        # 刪掉舊任務後創建新任務並存檔
                        with open('device_list.txt', 'w') as f:
                            f.write(device_list)
                else:
                    # 直接創新的
                    print("Create new device_list")
                    with open('device_list.txt', 'w') as f:
                        f.write(device_list)
        except IOError:
            # 檔案可能無法讀取或不存在
            # 直接創新的
            with open('device_list.txt', 'w') as f:
                f.write(device_list)
            print("Error: file no find or can not read")
            print("Create new device_list")
    else:
        # 沒有網路連線時
        print("Lost connect!")
        # lcd 顯示 Lost connect!
        pass


def Initializing(url, url1):
    global upload_url
    lcd_clearall()
    while True:
        lcd_print(0, 0, 2, "Initializing!        ")
        ble = ble_initializing()
        net = net_initializing(url1)
        if ble == "blef":
            lcd_print(0, 0, 0, "Initializing!        ")
            lcd_print(1, 0, 1, "BLE                  ")
            lcd_print(1, 4, 2, "ERROR!")
            lcd_print(1, 4, 1, "      ")
            lcd_print(1, 4, 2, "ERROR!")
            lcd_print(1, 0, 1, "                      ")
        if net == "netf":
            lcd_print(0, 0, 0, "Initializing!         ")
            lcd_print(1, 0, 1, "Net                   ")
            lcd_print(1, 4, 2, "ERROR!")
            lcd_print(1, 4, 1, "      ")
            lcd_print(1, 4, 2, "ERROR!")
            lcd_print(1, 0, 1, "                      ")
        if ble != "blef" and net != "netf":
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), end='  ')
            print("Upload Device's mac")
            sucess = 0
            fail = 0
            for x in ble:
                print(x)
                mac = "%s%s%s%s%s%s" % (
                    x[0:2], x[3:5], x[6:8], x[9:11], x[12:14], x[15:17])
                mac = "M"+mac
                #print (len(mac))
                if len(mac) == 13:  # 簡單的資料長度驗證
                    if upload_data(url, mac):
                        sucess += 1
                        #print ("s")
                    else:
                        fail += 1
                        #print ("f")
                time.sleep(0.1)
            print("Sucess: " + str(sucess) + " Fail: " + str(fail))
            if os.path.exists("schedule.txt"):
                # 刪掉暫存檔
                os.remove("schedule.txt")
                print("Remove old schedule.txt ")
            if os.path.exists("device_list.txt"):
                # 刪掉暫存檔
                os.remove("device_list.txt")
                print("Remove old device_list.txt ")
            break


if __name__ == "__main__":
    try:
        # Initializing(data_upload,url1)
        #os.system("sh autotask.sh")
        #os.system("screen -S servo -d -m bash -c 'python3 servo.py'")
        #sched.add_job(task1, 'interval', seconds=10)
        #sched.add_job(task, 'cron', id=str(10), hour=12,minute=50, kwargs={"mac": "11:15:85:00:4f:ee","tag": "e899e65f", "food_amount": "90.00"})
        #sched.add_job(BT_sync, 'cron', hour=6,minute=9, args=["env"])

        #sched.add_job(Schedule_sync, 'interval', seconds=10)
        sched.add_job(Device_sync, 'interval', seconds=10)
        #sched.add_job(BT_sync,'interval', seconds=61, args=["env"])
        #sched.add_job(BT_sync,'interval', seconds=121, args=["pet"])
        sched.add_job(BT_sync, 'interval', seconds=120, args=["all"])
        sched.start()

    except KeyboardInterrupt:
        os.system("screen -X -S servo quit")
        os.system("screen -X -S mjpg quit")
