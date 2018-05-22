from selenium import webdriver
from selenium.webdriver.support import wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import time
import xlwt
import os
from datetime import datetime


# 获取所有的打开页面的orderlist 和 datetimelist，但是检索要自己进行


def getlist(driver0):
    allorderlist = []
    alldatetimelist = []
    allOrderNameList = []
    currentpagination = 0
    while True:
        while True:
            # 获取当前页数的循环，如果发生了不可预知的错误，那么重新进行
            try:
                time.sleep(2)
                wait.WebDriverWait(driver0, 10000000).until(
                    EC.presence_of_element_located((By.ID, 'myo-table')))
                currentpagination1 = driver0.find_element_by_xpath("//strong[@class = 'currentpagination']").text
                if int(currentpagination1) == int(currentpagination) + 1:
                    break
            except Exception as e:
                print(e)
                pass

        # 匹配
        while True:
            try:
                orderlisthtml = wait.WebDriverWait(driver0, 10000000).until(
                    EC.presence_of_element_located((By.ID, 'myo-table')))
                pattern = re.compile(r'\d{3}-\d{7}-\d{7}')
                orderlist = re.findall(pattern, orderlisthtml.text)

                pattern0 = re.compile(r'_myoLO_\w{55}__product')
                orderNamelist = re.findall(pattern0, orderlisthtml.text)

                datelist = []
                timelist = []
                for i in orderlist:
                    currentordertable = driver0.find_element_by_id('row-' + i)
                    pattern1 = re.compile(r'\w{3} \d{1,2}, \d{4}')
                    thisdate = re.findall(pattern1, currentordertable.text)
                    datelist.append(thisdate[0])

                    pattern2 = re.compile(r'\d+:\d+:\d+ \w\w')
                    thistime = re.findall(pattern2, currentordertable.text)
                    timelist.append(thistime[0])

                #     把这一页的信息加入
                allorderlist.extend(orderlist)
                allOrderNameList.extend(orderNamelist)
                for i, j in zip(datelist, timelist):
                    # print('test:    '+i+'    '+j)
                    thisdatetime = datetime.strptime(i + ' ' + j, "%b %d, %Y %I:%M:%S %p")
                    alldatetimelist.append(thisdatetime)
                #     信息加入成功，那么可以离开这一页的try循环
                break
            except Exception as e:
                print(e)
                pass

        # 翻页

        try:
            nextpagebutton = driver0.find_element_by_xpath("//a[text()='Next' and @class = 'myo_list_orders_link']")
            currentpagination = driver0.find_element_by_xpath("//strong[@class = 'currentpagination']").text
            nextpagebutton.click()
            print("next")
        except Exception as e:
            print(e)
            print("finish")
            break
    print("``````````````")
    print(alldatetimelist)
    return allorderlist, alldatetimelist, allOrderNameList


# 尝试获取currentThreadSenderID，如果获取失败，那么返回的是none
def getcurrent(driver0, orderid):
    while True:
        try:
            time.sleep(2)
            wait.WebDriverWait(driver0, 5).until(
                EC.presence_of_element_located((By.ID, 'search-text-box')))
            idinput = driver0.find_element_by_id("search-text-box")
            idinput.clear()
            idinput.send_keys(orderid)
            searchbutton = driver0.find_element_by_name("Search")
            searchbutton.click()
            # 只有不出现任何问题，才能继续，否则重新来一遍
            break
        except Exception as e:
            print(e)
            pass
    try:
        # 等5秒，如果还没搜出来结果，那么肯定就是没有了，返回None
        time.sleep(2)
        wait.WebDriverWait(driver0, 3).until(
            EC.presence_of_element_located((By.ID, 'currentThreadSenderId')))
        current = driver0.find_element_by_id('currentThreadSenderId').get_attribute('value')
        return current
    except Exception as e:
        print(e)
        return None


def writeExcel(current, order, dateList):
    # excelname = str(month) + '-' + str(day) + 'to' + str(month2) + '-' + str(day2) + '.xls'
    # excelName = 'result.xls'
    # try:
    #     firstDay = dateList[0]
    #     lastDay = dateList[-1]
    #     assert isinstance(firstDay,datetime)
    #     assert isinstance(lastDay,datetime)
    #     excelName = str(firstDay.month)+'-'+str(firstDay.day)+'To'+\
    #                 str(lastDay.month)+'-'+str(lastDay.day)+'.xls'
    # except:
    now = datetime.now()
    excelName = '%d-%d-%d_%d.xls' % (now.month, now.day, now.hour, now.minute)

    # excelname = 'searchResult.xls'

    excelurl = os.path.join('.', excelName)

    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('test', cell_overwrite_ok=True)
    sheet.write(0, 0, 'currentThreadSenderId')
    sheet.write(0, 1, 'orderId')
    # sheet.write(0, 2, 'buyerName')
    sheet.write(0, 2, 'buyerDate')
    n = 1
    # for i, j, k, t in zip(current, order, name, date):
    for i, j, k in zip(current, order, dateList):
        sheet.write(n, 0, i)
        sheet.write(n, 1, j)
        sheet.write(n, 2, k.date().__str__())
        # sheet.write(n, 3, t)
        n += 1

    book.save(excelurl)  # 在字符串前加r，声明为raw字符串，这样就不会处理其中的转义了。否则，可能会报错
