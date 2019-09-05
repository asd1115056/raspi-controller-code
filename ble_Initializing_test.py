from RPLCD.i2c import CharLCD
import sys
import time
import smbus2
sys.modules['smbus'] = smbus2
from bluepy.btle import *
import threading

lcd = CharLCD('PCF8574', address=0x27, port=1, backlight_enabled=True)
suuid = UUID(0xffe0)
cuuid = UUID(0xffe1)
mac="11:15:85:00:4f:ee"

class MyDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

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


if __name__ == "__main__":
    ble_initializing()
