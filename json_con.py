import json
import demjson
import pickle
new=[{"Tag": "FDLMCW", "food_Name": "tamto", "schedule_time": "08:00:00", "food_amount": "50.00"}, {"Tag": "EAVBR1", "food_Name": "tamto", "schedule_time": "09:00:00", "food_amount": "50.00"}, {"Tag": "EAVBR1", "food_Name": "tamto", "schedule_time": "11:34:00", "food_amount": "50.00"}, {"Tag": "EAVBR1", "food_Name": "tamto", "schedule_time": "11:35:00", "food_amount": "50.00"}, {"Tag": "FDLMCW", "food_Name": "tamto", "schedule_time": "11:36:00", "food_amount": "50.00"}, {"Tag": "EAVBR1", 
"food_Name": "tamto", "schedule_time": "11:37:00", "food_amount": "30.00"}]
new1=[{"Tag": "FDLMCW", "food_Name": "tamto", "schedule_time": "08:00:00", "food_amount": "50.00"}, {"Tag": "EAVBR1", "food_Name": "tamto", "schedule_time": "09:00:00", "food_amount": "50.00"}, {"Tag": "EAVBR1", "food_Name": "tamto", "schedule_time": "11:34:00", "food_amount": "50.00"}, {"Tag": "EAVBR1", "food_Name": "tamto", "schedule_time": "11:35:00", "food_amount": "50.00"}, {"Tag": "FDLMCW", "food_Name": "tamto", "schedule_time": "11:36:00", "food_amount": "50.00"}, {"Tag": "EAVBR1", 
"food_Name": "tamto", "schedule_time": "11:37:00", "food_amount": "30.00"}]
with open('Scheduler_save.text','r') as f:
    output=eval(f.readline())
# output=json.dumps(output)
#output=json.loads(output)
#output=demjson.encode(output)

# output = output.replace("'", '"') 
#output = list(output)
#new=json.loads(new)
print(output)
print(type(output))
if output==new:
    print("Yes")
else:
    print("No")
#print(output)
#print(new)