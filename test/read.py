import time
fp = open('file.txt', "r")
line = fp.readline()
 
## 用 while 逐行讀取檔案內容，直至檔案結尾
while line:
    print (line)
    line = fp.readline()
    time.sleep(1)
 
fp.close()