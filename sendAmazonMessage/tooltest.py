from selenium import webdriver
from selenium.webdriver.support import wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import time
import xlwt
import os
from datetime import datetime


def outputexcel(month, day, month2, day2, current, order, name, date):

    excelname = str(month) + '-' + str(day) + 'to' + str(month2) + '-' + str(day2) + '.xls'
    # excelurl = os.path.join('.', excelname)
    excelurl = r'/Users/djc/Desktop/' + excelname
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('test', cell_overwrite_ok=True)
    sheet.write(0, 0, 'currentThreadSenderId')
    sheet.write(0, 1, 'orderId')
    sheet.write(0, 2, 'buyerName')
    sheet.write(0, 3, 'buyerDate')
    n = 1
    for i, j, k, t in zip(current, order, name, date):
        sheet.write(n, 0, i)
        sheet.write(n, 1, j)
        sheet.write(n, 2, k)
        sheet.write(n, 3, t)
        n += 1

    book.save(excelurl)  # 在字符串前加r，声明为raw字符串，这样就不会处理其中的转义了。否则，可能会报错
    return

# dt = datetime(2017,3,29,12,20)


def getlist(driver0):
    allorderlist = []
    alldatetimelist = []
    while True:
        time.sleep(2)
        orderlisthtml = wait.WebDriverWait(driver0, 10000000).until(
            EC.presence_of_element_located((By.ID, 'myo-table')))

        # 匹配
        pattern = re.compile(r'\d*-\d*-\d*')
        orderlist = re.findall(pattern, orderlisthtml.text)
        print(orderlist)
        allorderlist.extend(orderlist)

        pattern1 = re.compile(r'\w{3} \d, \d{4}')
        datelist = re.findall(pattern1, orderlisthtml.text)

        pattern2 = re.compile(r'\d+:\d+:\d+ \w\w')
        timelist = re.findall(pattern2, orderlisthtml.text)

        for i, j in zip(datelist, timelist):
            thisdatetime = datetime.strptime(i + ' ' + j, "%b %d, %Y %I:%M:%S %p")
            alldatetimelist.append(thisdatetime)
        # 翻页
        try:
            nextpagebutton = driver0.find_element_by_xpath("//a[text()='Next' and @class = 'myo_list_orders_link']")
            nextpagebutton.click()
            print("next")
        except Exception:
            print("finish")
            break
    print("``````````````")
    print(alldatetimelist)
    return allorderlist, alldatetimelist


# Configurations on Mac
url = r'file:///Users/djc/Downloads/4_files/7.html'
excelUrl = r'/Users/djc/Desktop/test1.xls'

driver = webdriver.Chrome('/Users/djc/Downloads/chromedriver')


# Configurations on Windows
# url = r'https://sellercentral.amazon.com/messaging/inbox'
# excelName = str(month) + '-' + str(day) +'to'+str(month2)+'-'+str(day2)+ '.xls'
# excelUrl = os.path.join('.', excelName)

# basePath = r'C:\Program Files (x86)\Google\Chrome\Application'
# path = os.path.join(basePath, 'chromedriver.exe')
# cOptions = webdriver.ChromeOptions()
# cOptions.add_argument(r'user-data-dir=C:\Users\pro\AppData\Local\Google\Chrome\User Data')
# driver = webdriver.Chrome(executable_path=path, options=cOptions)


print('ok?')
driver.get(url)
# AllOrderList, Alldatetimelist = getlist(driver)




# str1 = 'May 9, 2018 4:04:55 PM'
# dt = datetime.strptime(str1, "%b %d, %Y %I:%M:%S %p")
# print(dt)
orderlisthtml = wait.WebDriverWait(driver, 10000000).until(EC.presence_of_element_located((By.ID, 'myo-table')))

pattern11 = re.compile(r'Orders \d+ - \d+ of \d+')
pagefulltext = re.findall(pattern11, orderlisthtml.text)
pagetext = str(pagefulltext[0])
maxnum = pagetext.split()[-1]

# print(orderlisthtml.text)