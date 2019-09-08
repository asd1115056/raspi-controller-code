from RPLCD.i2c import CharLCD
import sys
import time
import smbus2

sys.modules['smbus'] = smbus2

lcd = CharLCD('PCF8574', address=0x27, port=1, backlight_enabled=True)

def lcd_clearline(line):
    lcd.cursor_pos = (line, 0)
    lcd.write_string("                ")
def lcd_print(line,postion,text):
    lcd.cursor_pos = (line, postion)
    lcd.write_string(text)

if __name__ == "__main__":
    try:
        print('按下 Ctrl-C 可停止程式')
        lcd.clear()
        while True:
            lcd_print(0,0,"Date: {}".format(time.strftime("%Y/%m/%d")))
            lcd_print(1,0,"Time: {}".format(time.strftime("%H:%M:%S")))
            lcd.cursor_pos = (0, 0)
            time.sleep(1)
    except KeyboardInterrupt:
        print('關閉程式')
    finally:
        lcd.clear()