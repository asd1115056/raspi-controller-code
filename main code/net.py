from lcd import *
import requests

url = 'http://localhost:8000/ajax/all_list_Schedule'

def net_initializing(url):
    statue=True
    while statue:
        lcd_clearall()
        lcd_print(0,0,"Net Initializing")
        lcd_print(1,0,"connect.....   ")
        time.sleep(2)
        try:
            response = requests.get(url)
            response.raise_for_status()
            lcd_print(1,0,"OK!          ")
            time.sleep(2)
            statue=False
        except requests.exceptions.RequestException:
            lcd_print(1,0,"FAIL!          ")
            time.sleep(2)
            lcd_countdown(1,20)
    lcd_clearall()


if __name__ == "__main__":
    net_initializing(url)
