from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import requests
import json
import logging

url1 = 'http://localhost:8000/ajax/all_list_Schedule22'

try:
    rep = requests.get(url1)
    rep.raise_for_status()
    print('1',rep.status_code)
except requests.exceptions.RequestException:
    print('2',rep.status_code)
