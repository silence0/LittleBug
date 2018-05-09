import datetime
import time

date1 = datetime.date(2018,5,11)
date2 = datetime.date(2018,5,7)
date3 = date1-date2
li = []
for i in range(0,date3.days+1):
    li.append(date2+datetime.timedelta(i))
if datetime.datetime(2017,1,1) in li:
    print('ok')