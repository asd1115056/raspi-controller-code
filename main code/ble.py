from bluepy.btle import *
from lcd import *
import signal
import time
from contextlib import contextmanager


service__uuid = "0000ffe0-0000-1000-8000-00805f9b34fb"
notify_uuid = "0000ffe1-0000-1000-8000-00805f9b34fb"
write_uuid = "0000ffe2-0000-1000-8000-00805f9b34fb"
ble_mac="11:15:85:00:4f:ee"
#ble_mac="11:15:85:00:4f:65"
ble_conn = None

class TimeoutException(Exception): pass

@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)

class MyDelegate(DefaultDelegate):
    def __init__(self, conn):
        DefaultDelegate.__init__(self)
        self.conn = conn
    def handleNotification(self, cHandle, data):
        global output
        try:
            output=data.decode("UTF-8")
        except UnicodeError:
            pass

def ble_connect(devAddr):
    global ble_conn
    #ble_conn = None
    if not devAddr is None and ble_conn is None:
        ble_conn = Peripheral(devAddr, ADDR_TYPE_PUBLIC)
        ble_conn.setDelegate(MyDelegate(ble_conn))
        #print("connected")

def ble_data(send): 
        global ble_conn,output,write_uuid,notify_uuid
        # write , set listen
        w = ble_conn.getCharacteristics(uuid=write_uuid)[0]
        w.write(bytes(send,"UTF-8"))
        #time.sleep(0.05)
        n = ble_conn.getCharacteristics(uuid=notify_uuid)[0]
        ble_conn.writeCharacteristic(n.valHandle+1, b"\x01\x00",True)
        # wait notification
        count=0
        while True:
             if  ble_conn.waitForNotifications(5.0):
                  locals()['X%s' % (count)]=output
                  count+=1 
                  continue
             else:
                  break
        temp=""
        for i in range(0,count):
             temp+= locals()['X%s' % (i)]
        return temp

def ble_disconnect():
    global ble_conn
    ble_conn.disconnect()
    ble_conn=None
    #print("disconnected")

def ble(mac,text):
    connect_timeout=15
    temp=None
    try:
        with time_limit(connect_timeout):
            ble_connect(mac)
            #time.sleep(0.05)
            temp=ble_data(text)
            ble_disconnect()
            return temp
    except TimeoutException as e:
        return "Timedout!"

def ble1(mac,text):
    ble_connect(mac)
    #time.sleep(0.05)
    temp=ble_data(text)
    ble_disconnect()
    return temp

def ble_scan():
    timeout=10.0
    scanner = Scanner().withDelegate(MyDelegate(None))
    devices = scanner.scan(timeout)
    for dev in devices:
            print("MAC:", dev.addr, " Rssi ", str(dev.rssi))
            try:
                with time_limit(15):
                    ble_connect(dev.addr)
                    time.sleep(0.025)
                    temp=ble_data("test")
                    print(temp)
                    ble_disconnect()
            except TimeoutException as e:
                    print("Timed out!")

def ble_initializing():
    i=1
    arr=[]
    scan_timeout=10
    connect_timeout=15
    lcd_clearall()
    lcd_print(0,0,0.5,"BLE Initializing") #(line,postion,delay,text)
    lcd_print(1,0,0,"Scanning.....    ")
    scanner = Scanner().withDelegate(MyDelegate(None))
    devices = scanner.scan(scan_timeout)
    lcd_print(1,0,1,"Find "+ str(len(devices)) +" Devices")
    for dev in devices:
            try:
                with time_limit(connect_timeout):
                    lcd_print(1,0,0.5,"Connecting....   ")
                    lcd_print(1,0,0.5,"Devices "+ str(i)+"     ")
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    print("MAC:", dev.addr, " Rssi ", str(dev.rssi))
                    ble_connect(dev.addr)
                    time.sleep(0.025)
                    temp=ble_data("test")
                    #print(temp)
                    ble_disconnect()
                    if temp=="ok":
                        arr.append(dev.addr)
                        lcd_print(1,0,1,"SUCCESS!           ")
                    else:
                        lcd_print(1,0,1,"FAIL!          ") 
            except TimeoutException as e:
                        lcd_print(1,0,1,"Timed out!         ")
            i+=1 
    #print("Done")
    lcd_clearall()
    if arr:
        return arr
    else:
        return "blef"

if __name__ == "__main__":
    arr=ble_initializing()
    print(arr)