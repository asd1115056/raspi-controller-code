import json

schedule_list = [{"Tag": "6d1cdf2b", "mac": "11:15:85:00:4f:ee", "schedule_time": "04:00:00", "food_amount": "15.00"}, {"Tag": "6d1cdf2b", "mac": "11:15:85:00:4f:ee", "schedule_time": "05:00:00", "food_amount": "10.00"}, {
    "Tag": "6d1cdf2b", "mac": "11:15:85:00:4f:ee", "schedule_time": "13:00:00", "food_amount": "10.00"}, {"Tag": "6d1cdf2b", "mac": "11:15:85:00:4f:ee", "schedule_time": "21:00:00", "food_amount": "22.00"}]
device_list = ["11:15:85:00:4f:ee", "11:15:85:00:4f:cc",
               "11:15:aa:50:4f:ee", "25:15:85:00:4f:ee"]


with open('device.txt', 'r') as f:
    a = f.readline()

a = eval(a)

for x in a:
    print(x)
    print(type(x))
