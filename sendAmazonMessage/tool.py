from selenium import webdriver
from selenium.webdriver.support import wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support import select
import re
import time
import xlwt
import os
from datetime import datetime
import traceback
from VAR import bMutex


# 获取所有的打开页面的orderlist 和 datetimelist，但是检索要自己进行


def getorderinfo(driver0, orderid):
    bMutex.lock()
    orderrow = driver0.find_element_by_id("row-" + orderid)
    orderinfo = orderrow.find_element_by_xpath("//span[contains(@id,'___product')]")
    o1 = orderinfo.text
    if (str(orderinfo.text)[-3:] == '...'):
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
    bMutex.unlock()
    return o1


def getorderinfo2(driver0, orderid):
    bMutex.lock()
    js = 'window.open(\"https://sellercentral.amazon.com/gp/orders-v2/details?orderID=' + orderid + '\");'
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
    bMutex.unlock()
    return o1

def getorderinfo3(driver0, orderid):
    bMutex.lock()
    js = 'window.open(\"https://sellercentral.amazon.com/gp/orders-v2/details?orderID=' + orderid + '\");'
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

    driver0.switch_to_window(handles[1])
    bMutex.unlock()
    return o1


def getlist(driver0):
    allorderlist = []
    alldatetimelist = []
    # allorderinfolist = []
    currentpagination = 0
    onepageflag = 0
    bMutex.lock()
    wait.WebDriverWait(driver0, 10000000).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "select[name='itemsPerPage']")))
    selectPagPer = select.Select(driver0.find_elements_by_name('itemsPerPage')[-1])
    selectPagPer.select_by_value('100')
    # assert isinstance(driver0, webdriver.Chrome)
    goButton = driver0.find_elements_by_css_selector("input[type='image'][width='21'")
    goButton = goButton[-1]
    goButton.click()
    bMutex.unlock()
    time.sleep(5)

    while True:
        # 最外层循环用来翻页

        # 获取当前页数的循环，如果发生了不可预知的错误，那么重新进行
        while True:
            try:
                time.sleep(2)
                bMutex.lock()
                orderlisthtml = wait.WebDriverWait(driver0, 10000000).until(
                    EC.presence_of_element_located((By.ID, 'myo-table')))
                bMutex.unlock()
                # 如果是刚开始，那么判断一下是不是只有一页（因为一页的时候网页排版不同）
                if currentpagination == 0:
                    time.sleep(3)
                    bMutex.lock()
                    pagefulltr = driver0.find_element_by_xpath("//div[@id='myo-table']/table/tbody/tr[1]")
                    bMutex.unlock()
                    # pattern11 = re.compile(r'Orders \d+ to \d+')
                    # pagefulltext = re.findall(pattern11, pagefulltr.text)
                    # pagetext = str(pagefulltext[0])
                    # maxnum = pagetext.split()[-1]
                    # print("pagenumberget:" + str(time.clock()))
                    # bMutex.unlock()
                    # if int(maxnum) <= 100:
                    if 'of' not in pagefulltr.text:
                        onepageflag = 1
                        print('onegage!')
                        break
                bMutex.lock()
                currentpagination1 = driver0.find_element_by_xpath("//strong[@class = 'currentpagination']").text
                bMutex.unlock()
                if int(currentpagination1) == int(currentpagination) + 1:
                    break
            except Exception as e:
                bMutex.unlock()
                traceback.print_exc()
                print('try again---------------------------------')

        # 匹配
        while True:
            try:
                bMutex.lock()
                orderlisthtml = wait.WebDriverWait(driver0, 10000000).until(
                    EC.presence_of_element_located((By.ID, 'myo-table')))
                orderlist = []
                datelist = []
                timelist = []
                allordertr = driver0.find_elements_by_xpath(
                    "//div[@id='myo-table']/table/tbody/tr[contains(@id,'row-')]")
                for i in allordertr:
                    orderid = str(i.get_attribute('id'))[-19:]
                    if re.match(re.compile('\d{3}-\d{7}-\d{7}'),orderid) == None:
                        continue
                    orderlist.append(orderid)
                    datetd = i.find_element_by_xpath("./td[2]")
                    # print(datetd.text)
                    thisdate = str(datetd.text).split('\n')
                    datelist.append(thisdate[0])
                    timelist.append(thisdate[1][:-4])
                # pattern = re.compile(r'\d{3}-\d{7}-\d{7}')
                # orderlist = re.findall(pattern, orderlisthtml.text)

                # orderinfolist = []
                print("allorderget:" + str(time.clock()))

                # for i in orderlist:
                #     currentordertable = driver0.find_element_by_id('row-' + i)
                #     pattern1 = re.compile(r'\w{3} \d{1,2}, \d{4}')
                #     thisdate = re.findall(pattern1, currentordertable.text)
                #     datelist.append(thisdate[0])
                #
                #     pattern2 = re.compile(r'\d+:\d+:\d+ \w\w')
                #     thistime = re.findall(pattern2, currentordertable.text)
                #     timelist.append(thistime[0])
                #
                # orderinfolist.append(getorderinfo(driver0,i))
                bMutex.unlock()
                #     把这一页的信息加入
                allorderlist.extend(orderlist)
                print("alldateget:" + str(time.clock()))
                # print(orderinfolist)
                # allorderinfolist.extend(orderinfolist)
                for i, j in zip(datelist, timelist):
                    # print('test:    '+i+'    '+j)
                    thisdatetime = datetime.strptime(i + ' ' + j, "%b %d, %Y %I:%M:%S %p")
                    alldatetimelist.append(thisdatetime)
                #     信息加入成功，那么可以离开这一页的try循环
                # todo:这一页成功了，那么记录成功页到文件中即可
                break
            except Exception as e:
                bMutex.unlock()
                traceback.print_exc()
                print('try again----------------------------')

        # 翻页
        if onepageflag == 1:
            break

        try:
            bMutex.lock()
            nextpagebutton = driver0.find_element_by_xpath("//a[text()='Next' and @class = 'myo_list_orders_link']")
            currentpagination = driver0.find_element_by_xpath("//strong[@class = 'currentpagination']").text
            nextpagebutton.click()
            bMutex.unlock()
            print("next")
        except Exception as e:
            bMutex.unlock()
            # traceback.print_exc()
            print("finish to get orderID---------------------")
            print("finish:" + str(time.clock()))
            break
    return allorderlist, alldatetimelist


# 尝试获取currentThreadSenderID，如果获取失败，那么返回的是none
def getcurrent(driver0, orderid):
    while True:
        try:
            time.sleep(2)
            bMutex.lock()
            wait.WebDriverWait(driver0, 5).until(
                EC.presence_of_element_located((By.ID, 'search-text-box')))
            idinput = driver0.find_element_by_id("search-text-box")
            searchbutton = driver0.find_element_by_name("Search")
            # idinput.clear()
            # idinput.send_keys(orderid)
            driver0.execute_script("arguments[0].value=" + "'" + orderid + "'", idinput)
            driver0.execute_script('arguments[0].click();', searchbutton)
            # searchbutton.click()
            # 只有不出现任何问题，才能继续，否则重新来一遍
            bMutex.unlock()
            break
        except Exception as e:
            bMutex.unlock()
            traceback.print_exc()
            print('try again--------------------')

    try:
        # 等5秒，如果还没搜出来结果，那么肯定就是没有了，返回None
        time.sleep(2)
        bMutex.lock()
        idDom = wait.WebDriverWait(driver0, 3).until(
            EC.presence_of_element_located((By.ID, 'currentThreadSenderId')))
        current = idDom.get_attribute('value')
        bMutex.unlock()
        return current
    except Exception as e:
        # traceback.print_exc()

        bMutex.unlock()
        print('No result found, ready to send message')
        return None


def getcurrent2(driver0, orderid,lastcurrentid,lastorderid):

        while True:
            try:
                bMutex.lock()
                wait.WebDriverWait(driver0, 5).until(
                    EC.presence_of_element_located((By.ID, 'search-text-box')))
                idinput = driver0.find_element_by_id("search-text-box")
                searchbutton = driver0.find_element_by_name("Search")
                # idinput.clear()
                # idinput.send_keys(orderid)
                driver0.execute_script("arguments[0].value=" + "'" + orderid + "'", idinput)
                driver0.execute_script('arguments[0].click();', searchbutton)
                # searchbutton.click()
                # 只有不出现任何问题，才能继续，否则重新来一遍
                bMutex.unlock()
                break
            except Exception as e:
                bMutex.unlock()
                traceback.print_exc()
                print('try again--------------------')

        while True:
            try:
                # 等5秒，如果还没搜出来结果，那么肯定就是没有了，返回None
                bMutex.lock()
                idDom = wait.WebDriverWait(driver0, 3).until(
                        EC.presence_of_element_located((By.ID, 'currentThreadSenderId')))
                current = str(idDom.get_attribute('value'))
                bMutex.unlock()
                if current == lastcurrentid:
                    bMutex.lock()
                    orderidA = wait.WebDriverWait(driver0, 3).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "a[href^='/gp/orders-v2/details?ie=UTF8&orderID=']")))
                    thisorderid = str(orderidA.get_attribute('href')[-19:])
                    bMutex.unlock()
                    if thisorderid == orderid:
                        bMutex.lock()
                        idDom = wait.WebDriverWait(driver0, 3).until(
                            EC.presence_of_element_located((By.ID, 'currentThreadSenderId')))
                        current = str(idDom.get_attribute('value'))
                        bMutex.unlock()
                        return current
                else:
                    return current
            except Exception as e:
                # traceback.print_exc()
                try:
                    wait.WebDriverWait(driver0, 3).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'click-thread')))
                    bMutex.unlock()
                except Exception as ee:
                    bMutex.unlock()
                    print('No result found, ready to send message')
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
    startDate = dateList[-1]
    endDate = dateList[0]
    excelName = '%d-%d_%d-%d.xls' % (startDate.month,startDate.day,endDate.month,endDate.day)

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
