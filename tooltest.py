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
# url = r'file:///Users/djc/Downloads/4_files/7.html'
print("start:" + str(time.clock()))


if '1111' == 0:
    print('1111')


# url = r'file:///Users/djc/Desktop/spider/Manage%20Orders%20-%20Amazon.html'
url = r'file:///Users/djc/Desktop/spider/%E7%94%A8%E6%89%80%E9%80%89%E9%A1%B9%E7%9B%AE%E6%96%B0%E5%BB%BA%E7%9A%84%E6%96%87%E4%BB%B6%E5%A4%B9/succ.html?cs=39426419&fi=RESPONSE_NEEDED'
excelUrl = r'/Users/djc/Desktop/test1.xls'
#
# driver = webdriver.Chrome('/Users/djc/Downloads/chromedriver')
# print("chrome ready:" + str(time.clock()))

# Configurations on Windows
# url = r'https://sellercentral.amazon.com/messaging/inbox'
# excelName = str(month) + '-' + str(day) +'to'+str(month2)+'-'+str(day2)+ '.xls'
# excelUrl = os.path.join('.', excelName)

# basePath = r'C:\Program Files (x86)\Google\Chrome\Application'
# path = os.path.join(basePath, 'chromedriver.exe')
# cOptions = webdriver.ChromeOptions()
# cOptions.add_argument(r'user-data-dir=C:\Users\pro\AppData\Local\Google\Chrome\User Data')
# driver = webdriver.Chrome(executable_path=path, options=cOptions)


# print('ok?')
# driver.get(url)
# AllOrderList, Alldatetimelist = getlist(driver)


# orderidA = wait.WebDriverWait(driver, 3).until(
#     EC.presence_of_element_located((By.ID, 'spaui-home')))
# thisorderid = str(orderidA.get_attribute('href'))[-20:-1]
# print(thisorderid)
# oriii = '111-2300471-3237033'
# if thisorderid == oriii:
#     print('11111111111')

# nomessagespan = wait.WebDriverWait(driver, 3).until(
#     EC.presence_of_element_located((By.CSS_SELECTOR, "a[href^='https://sellercentral.amazon.com/gp/communication-manager/i']")))
#
# print(nomessagespan.text)

# nomes = str(nomessagespan.get_attribute('class'))[-7:]
# if nomes == 'visible':
#     print("ssssssss")


# str1 = 'May 9, 2018 4:04:55 PM'
# dt = datetime.strptime(str1, "%b %d, %Y %I:%M:%S %p")
# print(dt)

# orderlisthtml = wait.WebDriverWait(driver, 10000000).until(EC.presence_of_element_located((By.ID, 'myo-table')))
# print("html ready:" + str(time.clock()))
# pagefulltr = driver.find_element_by_xpath("//div[@id='myo-table']/table/tbody/tr[1]")
# pattern11 = re.compile(r'Orders \d+ - \d+ of \d+')
# pagefulltext = re.findall(pattern11, pagefulltr.text)
# pagetext = str(pagefulltext[0])
# maxnum = pagetext.split()[-1]
# print("pagenumber get:" + str(time.clock()))
# print(maxnum)
# orderlist = []
# datelist = []
# timelist = []
# allordertr = driver.find_elements_by_xpath("//div[@id='myo-table']/table/tbody/tr[contains(@id,'row-')]")
#
# for i in allordertr:
#     orderid = str(i.get_attribute('id'))[-19:]
#     orderlist.append(orderid)
#     datetd = i.find_element_by_xpath("./td[2]")
#     # print(datetd.text)
#     thisdate = str(datetd.text).split('\n')
#     datelist.append(thisdate[0])
#     timelist.append(thisdate[1])
# print(orderlist)
# print(len(orderlist))
# print("all order and date get:" + str(time.clock()))

# for i in orderlist:
#     currentordertable = driver.find_element_by_id('row-' + i)
#     pattern1 = re.compile(r'\w{3} \d{1,2}, \d{4}')
#     thisdate = re.findall(pattern1, currentordertable.text)
#     datelist.append(thisdate[0])
#
#     pattern2 = re.compile(r'\d+:\d+:\d+ \w\w')
#     thistime = re.findall(pattern2, currentordertable.text)
#     timelist.append(thistime[0])
#     # print("dateget:" + str(time.clock()))
#     #
#     # orderinfolist.append(getorderinfo(driver0,i))
# #     把这一页的信息加入
# print("alldateget:" + str(time.clock()))
# orderinfo = driver.find_elements_by_xpath("//span[contains(@id,'___product')]")
# info_a = driver.find_element_by_xpath("//a[contains(@href,'orderId=111-2389060-6443420')]")
# info_a = driver.find_element_by_link_text("111-2389060-6443420")
# print(info_a)
# info_a.click()
#
# for i in orderinfo:
#     print("i: " + i.text)





def getorderinfo(driver0,orderid):
    orderrow = driver.find_element_by_id("row-"+orderid)
    orderinfo = orderrow.find_element_by_xpath("//span[contains(@id,'___product')]")
    o1 = orderinfo.text
    if(str(orderinfo.text)[-3:] == '...'):
        info_a = orderrow.find_element_by_link_text(orderid)
        js = 'window.open(\"' + info_a.get_attribute('href') + '\");'
        handle = driver0.current_window_handle
        driver0.execute_script(js)

        handles = driver0.window_handles
        for newhandle in handles:

            # 筛选新打开的窗口B

            if newhandle != handle:

        # 切换到新打开的窗口B

                driver0.switch_to_window(newhandle)

        # 在新打开的窗口B中操作
        wait.WebDriverWait(driver0, 10000000).until(
            EC.presence_of_element_located((By.ID, 'myo-order-details-item-product-details')))
        o1 = driver0.find_element_by_xpath("//a[contains(@href,'https://www.amazon.com/gp/product/')]").text

        # 关闭当前窗口B

        driver0.close()

        # 切换回窗口A

        driver0.switch_to_window(handles[0])

    return o1


# print(getorderinfo(driver, '112-7159011-6004236'))




# print(orderlisthtml.text)