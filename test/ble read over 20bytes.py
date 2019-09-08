from RPLCD.i2c import CharLCD
import sys
import time
import smbus2
sys.modules['smbus'] = smbus2
from bluepy.btle import *
import threading

lcd = CharLCD('PCF8574', address=0x27, port=1, backlight_enabled=True)
service__uuid = "0000ffe0-0000-1000-8000-00805f9b34fb"
notify_uuid = "0000ffe1-0000-1000-8000-00805f9b34fb"
write_uuid = "0000ffe2-0000-1000-8000-00805f9b34fb"
ble_mac="11:15:85:00:4f:ee"
ble_conn = None
device=None

class MyDelegate(DefaultDelegate):
    def __init__(self, conn):
        DefaultDelegate.__init__(self)
        self.conn = conn

    def handleNotification(self, cHandle, data):
        global c
        data = data.decode("UTF-8")
        c=data

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            pass
        elif isNewData:   
            print("\\nDiscovery:", "MAC:", dev.addr, " Rssi ", str(dev.rssi))

def ble_connect(devAddr):
    global ble_conn
    if not devAddr is None and ble_conn is None:
        ble_conn = Peripheral(devAddr, ADDR_TYPE_PUBLIC)
        time.sleep(0.5)
        #ble_conn.setMTU(20)
        ble_conn.setDelegate(MyDelegate(ble_conn))
        print("connected")


def ble_disconnect():
    global ble_conn
    ble_conn.disconnect()
    print("disconnected")

if __name__ == '__main__':
    # scan 
    scanner = Scanner().withDelegate(MyDelegate(None))
    timeout = 1.0
    devices = scanner.scan(timeout)
    for dev in devices:
        if dev.addr == ble_mac:
            print("\\nDiscovery:", "MAC:", dev.addr, " Rssi ", str(dev.rssi))
            for (adtype, desc, value) in dev.getScanData():
                print ("  %s(0x%x) = %s" % (desc, int(adtype), value))
            device=True
            break
        else:
            device=False
    if device==False:
        print ("BLE NO FIND!")
    else:   
        # connect  
        ble_connect(ble_mac)
        # write , set listen
        w = ble_conn.getCharacteristics(uuid=write_uuid)[0]
        w.write(bytes("test","UTF-8"))
        n = ble_conn.getCharacteristics(uuid=notify_uuid)[0]
        ble_conn.writeCharacteristic(n.valHandle+1, b"\x01\x00",True)

        # wait notification
        count=0
        while True:
             if  ble_conn.waitForNotifications(1.0):
                  locals()['X%s' % (count)]=c
                  count+=1 
                  continue
             else:
                  break
        temp=""
        for i in range(0,count):
             temp+= locals()['X%s' % (i)]
        print(temp)
        print(count)

        with open('test.txt', 'w') as f:
            f.write(temp)
        ble_disconnect()


