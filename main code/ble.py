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
    print("disconnected")

def ble_scan():
    global timeout,ble_mac
    scanner = Scanner().withDelegate(MyDelegate())
    devices = scanner.scan(timeout)
    for dev in devices:
        if dev.addr == ble_mac:
            print("\\nDiscovery:", "MAC:", dev.addr, " Rssi ", str(dev.rssi))
            for (adtype, desc, value) in dev.getScanData():
                print ("  %s(0x%x) = %s" % (desc, int(adtype), value))
            return True
            break
        else:
            print ("ble_scan:DEVICE NO FOUND")
            return False

def ble_data(send,timeout): 
        global ble_conn,output,write_uuid,notify_uuid
        # write , set listen
        w = ble_conn.getCharacteristics(uuid=write_uuid)[0]
        w.write(bytes(send,"UTF-8"))
        time.sleep(0.05)
        n = ble_conn.getCharacteristics(uuid=notify_uuid)[0]
        ble_conn.writeCharacteristic(n.valHandle+1, b"\x01\x00",True)
        # wait notification
        count=0
        while True:
             if  ble_conn.waitForNotifications(timeout):
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

def ble(text,timeout):
    global ble_mac
    ble_connect(ble_mac)
    time.sleep(0.025)
    temp=ble_data(text,timeout)
    ble_disconnect()
    return temp

def ble_initializing():
    timeout = 5.0
    statue=True
    while statue:
        lcd_clearall()
        lcd_print(0,0,"BLE Initializing")
        lcd_print(1,0,"Scan.....       ")
        scanner = Scanner().withDelegate(MyDelegate(None))
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
            lcd_print(1,0,"FAIL!          ")
            time.sleep(2)
            lcd_countdown(1,20)
        else:
            if ble("text")=="ok":
                print ("ble_initializing:SUCESSFUL")
                lcd_print(1,0,"OK!        ")
                time.sleep(2)
                statue=False
            else:
                print ("ble_initializing:FAIL")
                lcd_print(1,0,"FAIL!       ")
                time.sleep(2)
                lcd_countdown(1,20)       
    lcd_clearall()

if __name__ == "__main__":
    ble_initializing()
    print (ble("test",5))
   
