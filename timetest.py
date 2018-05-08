import datetime
import time

# print time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()) 

now = datetime.datetime.now()
date = now + datetime.timedelta(days = -1)
e = time.localtime(time.time())

print (date.strftime("date:%b %d"))

month = date.strftime("%b")
day = int(date.strftime("%d"))

print (month,"   ",day)

s = "May 7"
str = s.split()
print (str)
if str[0] == month and int(str[1]) == day:
	print ("sssss")

# print ("本地时间为 :", e)




if e.tm_hour == 0 and e.tm_min == 0 and e.tm_sec == 0:
	print ("ok")
else:
	print ("not ok")



