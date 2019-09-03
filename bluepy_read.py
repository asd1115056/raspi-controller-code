from bluepy.btle import *

suuid = UUID(0xffe0)
cuuid = UUID(0xffe1)
setup_data = b"\x01\x00"
mac="11:15:85:00:4f:ee"
# suuid="0000ffe0-0000-1000-8000-00805f9b34fb"
# chara_uuid="0000ffe1-0000-1000-8000-00805f9b34fb"


class MyDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
        # ... initialise here

    def handleNotification(self, cHandle, data):
        print(data)
        # ... perhaps check cHandle
        # ... process 'data'


p = Peripheral(mac)
p.setDelegate(MyDelegate())
print("connected")

u = p.getServiceByUUID(suuid)
ch = u.getCharacteristics(cuuid)[0]
desc = ch.getDescriptors()[0]
desc.write(b"\x01\x00", True)
print("writing done")

while True:
    if p.waitForNotifications(1.0):
        # handleNotification() was called
        # print("Notify")
        continue
    # print ("Waiting...")
    # Perhaps do something else here
