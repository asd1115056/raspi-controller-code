import json

new=[{"Tag": "FDLMCW", "food_Name": "tamto", "schedule_time": "08:00:00", "food_amount": "50.00"}, {"Tag": "EAVBR1", "food_Name": "tamto", "schedule_time": "09:00:00", "food_amount": "50.00"}, {"Tag": "EAVBR1", "food_Name": "tamto", "schedule_time": "11:34:00", "food_amount": "50.00"}, {"Tag": "EAVBR1", "food_Name": "tamto", "schedule_time": "11:35:00", "food_amount": "50.00"}, {"Tag": "FDLMCW", "food_Name": "tamto", "schedule_time": "11:36:00", "food_amount": "50.00"}, {"Tag": "EAVBR1", 
"food_Name": "tamto", "schedule_time": "11:37:00", "food_amount": "30.00"}]
new1=[{"Tag": "FDLMCW", "food_Name": "tamto", "schedule_time": "08:00:00", "food_amount": "50.00"}, {"Tag": "EAVBR1", "food_Name": "tamto", "schedule_time": "09:00:00", "food_amount": "50.00"}, {"Tag": "EAVBR1", "food_Name": "tamto", "schedule_time": "11:34:00", "food_amount": "50.00"}, {"Tag": "EAVBR1", "food_Name": "tamto", "schedule_time": "11:35:00", "food_amount": "50.00"}, {"Tag": "FDLMCW", "food_Name": "tamto", "schedule_time": "11:36:00", "food_amount": "50.00"}, {"Tag": "EAVBR1", 
"food_Name": "tamto", "schedule_time": "11:37:00", "food_amount": "30.00"}]
file_name='Scheduler_save.text'
with open('Scheduler_save.text','r') as f:
    output=eval(f.readline())

print(type(len(new)))
