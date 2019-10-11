from bluepy.btle import *
import signal
from contextlib import contextmanager

service__uuid = "0000ffe0-0000-1000-8000-00805f9b34fb"
notify_uuid = "0000ffe1-0000-1000-8000-00805f9b34fb"
write_uuid = "0000ffe2-0000-1000-8000-00805f9b34fb"
ble_mac="11:15:85:00:4f:ee"
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
    if not devAddr is None and ble_conn is None:
        ble_conn = Peripheral(devAddr, ADDR_TYPE_PUBLIC)
        ble_conn.setDelegate(MyDelegate(ble_conn))
        #print("connected")

def ble_disconnect():
    global ble_conn
    ble_conn.disconnect()
    ble_conn=None
    #print("disconnected")

def ble_scan():
    timeout=10.0
    scanner = Scanner().withDelegate(MyDelegate(None))
    devices = scanner.scan(timeout)
    for dev in devices:
            print("MAC:", dev.addr, " Rssi ", str(dev.rssi))
            try:
                with time_limit(10):
                    ble_connect(dev.addr)
                    time.sleep(0.025)
                    temp=ble_data("test")
                    print(temp)
                    ble_disconnect()
            except TimeoutException as e:
                    print("Timed out!")


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
        
if __name__ == "__main__":
    ble_scan()