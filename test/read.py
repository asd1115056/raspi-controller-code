import time
import datetime
fp = open('env.txt', "r")
line = fp.readline()
 
## 用 while 逐行讀取檔案內容，直至檔案結尾
while line:
    #print (line[2:11])
    print(datetime.datetime(2000, 1, 1, 12, 0) + datetime.timedelta(seconds=int(line[2:11])))
    line = fp.readline()
    time.sleep(1)
 
fp.close()