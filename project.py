from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import requests
import json
import os
import time
import ntplib
from RPLCD.i2c import CharLCD
import sys
import smbus2
from bluepy.btle import *


sys.modules['smbus'] = smbus2
lcd = CharLCD('PCF8574', address=0x27, port=1, backlight_enabled=False)
url1 = 'http://localhost:8000/ajax/all_list_Schedule'
suuid = UUID(0xffe0)
cuuid = UUID(0xffe1)
mac="11:15:85:00:4f:ee"
sched = BlockingScheduler()
count = 0

class MyDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
        # ... initialise here

    def handleNotification(self, cHandle, data):
        global temp
        temp=data.decode("ascii")
        # ... perhaps check cHandle
        # ... process 'data'

def Notify():
    p = Peripheral(mac)
    p.setDelegate(MyDelegate())
    print("connected")
    u = p.getServiceByUUID(suuid)
    ch = u.getCharacteristics(cuuid)[0]
    desc = ch.getDescriptors()[0]
    ch.write(bytes("t","ascii"))
    desc.write(b"\x01\x00", True)
    print("writing done")
    p.waitForNotifications(1.0)

def ble_initialization():
    statue=True
    while statue:
        try:
            p = Peripheral(mac)
            p.setDelegate(MyDelegate())
            u = p.getServiceByUUID(suuid)
            ch = u.getCharacteristics(cuuid)[0]
            desc = ch.getDescriptors()[0]
            desc.write(b"\x01\x00", True)
            ch.write(bytes("t","ascii"))
            if p.waitForNotifications(1.0):
                if temp=='ok':
                    statue=False
                    print("skip")
        except BTLEException:
            print("fail:wait for 40 sec")

def net_initialization():
    statue=True
    global url1
    while statue:
        try:
            response = requests.get(url1)
            response.raise_for_status()
            statue=False
        except requests.exceptions.RequestException:
            print("fail:wait for 40 sec")
            time.sleep(40)

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


def sync():
    global url1, sched, count
    new = []
    try:
        response = requests.get(url1)
        response.raise_for_status()
        r = json.loads(response.text)
        for di in r:
            new.append(di['fields'])
        if count == 0:
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
            if count == 0:
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
