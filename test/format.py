msg1 = 'e111585004fee6224266200240005400'
msg2 = 'p111585004fee6224266206d1cdf2b0988700000'
mac = '%s:%s:%s:%s:%s:%s' % (
    msg1[1:3], msg1[3:5], msg1[5:7], msg1[7:9], msg1[9:11], msg1[11:13])
time = msg1[13:22]
temperature = '%s.%s' % (msg1[22:25], msg1[25:27])
humidity = '%s.%s' % (msg1[27:30], msg1[30:32])
tag = msg2[22:30]
f = float('%s.%s' % (msg2[30:33], msg2[33:35]))
w = '%s.%s' % (msg2[35:38], msg2[38:41])
print(f)
print(w)
