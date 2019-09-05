import time
import requests
import sys
import smbus2
 
sys.modules['smbus'] = smbus2
 
from RPLCD.i2c import CharLCD

url1 = 'http://localhost:8000/ajax/all_list_Schedule'
lcd = CharLCD('PCF8574', address=0x27, port=1, backlight_enabled=True)

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

if __name__ == "__main__":
    net_initializing()
