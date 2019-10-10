from bluepy.btle import *
from lcd import *

service__uuid = "0000ffe0-0000-1000-8000-00805f9b34fb"
notify_uuid = "0000ffe1-0000-1000-8000-00805f9b34fb"
write_uuid = "0000ffe2-0000-1000-8000-00805f9b34fb"
ble_mac="11:15:85:00:4f:ee"
#ble_mac="11:15:85:00:4f:65"
ble_conn = None

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
    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            pass
        elif isNewData:   
            print("\\nDiscovery:", "MAC:", dev.addr, " Rssi ", str(dev.rssi))

def ble_connect(devAddr):
    global ble_conn,ble_mac
    if not devAddr is None and ble_conn is None:
        ble_conn = Peripheral(devAddr, ADDR_TYPE_PUBLIC)
        ble_conn.setDelegate(MyDelegate(ble_conn))
        print("connected")

def ble_disconnect():
    global ble_conn
    ble_conn.disconnect()
    ble_conn=None
    print("disconnected")

def ble_scan():
    global timeout,ble_mac
    scanner = Scanner().withDelegate(MyDelegate())
    devices = scanner.scan(timeout)
    for dev in devices:
            print("\\nDiscovery:", "MAC:", dev.addr, " Rssi ", str(dev.rssi))
            for (adtype, desc, value) in dev.getScanData():
                print ("  %s(0x%x) = %s" % (desc, int(adtype), value))

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
        #print(temp)
        #print(count)
        return temp

def ble(text):
    global ble_mac
    ble_connect(ble_mac)
    time.sleep(0.025)
    temp=ble_data(text)
    ble_disconnect()
    return temp


if __name__ == "__main__":
    print (ble("test"))
   
