from RPLCD.i2c import CharLCD
import sys
import time
import smbus2

sys.modules['smbus'] = smbus2

lcd = CharLCD('PCF8574', address=0x27, port=1, backlight_enabled=True)
def lcd_clearall():
    lcd.clear()
def lcd_clearline(line):
    lcd.cursor_pos = (line, 0)
    lcd.write_string("                ")
def lcd_print(line,postion,text):
    lcd.cursor_pos = (line, postion)
    lcd.write_string(text)
def lcd_countdown(line,timer):
    lcd_print(line,0,"Retry After")
    while timer>-1:
        lcd_print(line,13,"  s")
        if timer<10:
            lcd_print(line,14,str(timer))
        else:
            lcd_print(line,13,str(timer))
        timer-=1
        time.sleep(1)
def lcd_dot(line,postion,long,timer):
    begin=postion
    while timer>-1:
        lcd.cursor_pos = (line, postion)
        lcd.write_string(".               ")
        postion+=1
        timer-=0.5 
        time.sleep(0.5)
        if postion-begin>long:
            postion=begin


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