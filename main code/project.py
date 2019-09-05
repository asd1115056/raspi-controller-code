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
lcd = CharLCD('PCF8574', address=0x27, port=1, backlight_enabled=True)
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
        try:
            temp=data.decode("UTF-8")
        except UnicodeError:
            None

def ble_initializing():
    statue=True
    while statue:
        dot=3
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string("BLE Initializing")
        lcd.cursor_pos = (1, 0)
        lcd.write_string("BLE            ")
        while dot>-1:
            lcd.cursor_pos = (1, 3)
            if dot==2:
                lcd.write_string(".")
            if dot==1:
                lcd.write_string("..")
            if dot==0:
                lcd.write_string("...")
            time.sleep(1)
            dot-=1
        try:
            p = Peripheral(mac)
            p.setDelegate(MyDelegate())
            u = p.getServiceByUUID(suuid)
            ch = u.getCharacteristics(cuuid)[0]
            desc = ch.getDescriptors()[0]
            desc.write(b"\x01\x00", True)
            ch.write(bytes("t","UTF-8"))
            if p.waitForNotifications(1.0):
                if temp=='ok':
                    statue=False
                    lcd.cursor_pos = (1, 7)
                    lcd.write_string("OK!")
                    time.sleep(3)
                else:
                    lcd.cursor_pos = (1, 7)
                    lcd.write_string("FAIL!")
                    time.sleep(3)
            p.disconnect()
        except BTLEException:
            status=True
            lcd.cursor_pos = (1, 7)
            lcd.write_string("FAIL!")
            print("error")
            time.sleep(3)
        finally:
            lcd.clear()

def net_initializing():
    statue=True
    global url1
    while statue:
        timer=30
        dot=4
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string("Net Initializing")
        lcd.cursor_pos = (1, 0)
        lcd.write_string("Net")
        while dot>0:
            lcd.cursor_pos = (1, 3)
            if dot==3:
              lcd.write_string(".")
            if dot==2:
              lcd.write_string("..")
            if dot==1:
              lcd.write_string("...")
            time.sleep(1)
            dot-=1
        try:
            response = requests.get(url1)
            response.raise_for_status()
            lcd.cursor_pos = (1, 7)
            lcd.write_string("OK!")
            time.sleep(3)
            statue=False
        except requests.exceptions.RequestException:
            lcd.cursor_pos = (1, 7)
            lcd.write_string("FAIL!")
            time.sleep(3)
            lcd.cursor_pos = (1, 0)
            lcd.write_string("Retry After")
            while timer>-1:
                lcd.cursor_pos = (1,13)
                lcd.write_string("  s")
                if timer<10:
                    lcd.cursor_pos = (1,14)
                else:
                    lcd.cursor_pos = (1,13)
                lcd.write_string(str(timer))
                #print(timer)
                timer-=1
                time.sleep(1)
        finally:
            lcd.clear()

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
    net_initializing()
    ble_initializing()
    sched.add_job(sync, 'interval', seconds=5)
    sched.start()
