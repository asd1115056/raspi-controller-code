#from ble,lcd,net,sch,servo
import sys
import os
import time

ip=sys.argv[1]
url = 'http://'+ip+'/ajax/all_list_Schedule'
data_upload = 'http://'+ip+'/api/data_upload'
servo='http://'+ip+'/api/control_output'
schedule_list_url = 'http://'+ip+'/api/schedule_list'
device_list_url = 'http://'+ip+'/api/device_list'

test_url='https://www.google.com.tw/webhp?hl=zh-TW'

Initializing()
os.system("sh autotask.sh")
#os.system("screen -d -m bash -c 'python3 servo.py'")
sched.add_job(Schedule_sync, 'interval', seconds=10,args=["schedule_list_url"])
sched.add_job(Device_sync, 'interval', seconds=10,args=["device_list_url"])
sched.add_job(BT_sync,'interval', seconds=61, args=["env","data_upload"])
sched.add_job(BT_sync,'interval', seconds=121, args=["pet","data_upload"])
#sched.add_job(BT_sync_all,'interval', seconds=60, args=["data_upload"])
sched.start()
 
while True:
    try:
        control_command=control('servo')
        if control_command:
            Servo_move_test(control_command)
    except :
        pass
    time.sleep(0.5)