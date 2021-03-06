# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support import wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import datetime
import os
import re
import time
import xlwt
import getpass


def getDatas(year, month, day, year2, month2, day2):
    basePath = r'C:\Program Files (x86)\Google\Chrome\Application'

    path = os.path.join(basePath, 'bindriver.exe')
    cOptions = webdriver.ChromeOptions()

    cOptions.add_argument(r'user-data-dir=C:\Users\%s\AppData\Local\Google\Chrome\User Data'%(getpass.getuser()))
    driver = webdriver.Chrome(executable_path=path, options=cOptions)

    # driver = webdriver.Chrome('/Users/djc/Downloads/chromedriver')
    url = r'https://sellercentral.amazon.com/messaging/inbox'
    # url = r'file:///Users/djc/Downloads/Amazon.html'
    # excelUrl = r'/Users/djc/Desktop/test1.xls'
    excelName = str(month) + '-' + str(day) +'to'+str(month2)+'-'+str(day2)+ '.xls'
    excelUrl = os.path.join('.', excelName)

    print('ok?')

    # web.get()
    driver.get(url)
    returnAllMessage = wait.WebDriverWait(driver, 10000000).until(
        EC.presence_of_element_located((By.ID, 'current-filter-text')))

    # returnAllMessage = web.find_element_by_id('current-filter-text')
    returnAllMessage.click()

    allMessage = wait.WebDriverWait(driver, 10000000).until(
        EC.presence_of_element_located((By.LINK_TEXT, 'All Messages')))
    # allMessage = driver.find_element_by_link_text('All Messages')
    allMessage.click()

    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('test', cell_overwrite_ok=True)
    sheet.write(0, 0, 'currentThreadSenderId')
    sheet.write(0, 1, 'orderId')
    sheet.write(0, 2, 'buyerName')
    sheet.write(0, 3, 'buyerDate')
    n = 1
    index = 1
    dateStart = datetime.date(year,month,day)
    dateEnd = datetime.date(year2,month2,day2)
    selectDateObjList = []
    for i in range(0,(dateEnd-dateStart).days+1):
        selectDateObjList.append(dateStart+datetime.timedelta(i))
    stop = False
    while True:
        time.sleep(2)
        wait.WebDriverWait(driver, 10000).until(EC.visibility_of_element_located((By.ID, 'threads-list')))
        list = driver.find_element_by_id('threads-list')
        # time.sleep(2)
        t1 = wait.WebDriverWait(driver, 10000).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[class*='a-size-small thread-subject']")))
        print(t1.text)
        # time.sleep(3)
        allLetterTitleElements = list.find_elements_by_css_selector("[class*='a-size-small thread-subject']")
        wait.WebDriverWait(driver, 10000).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[class*='a-size-small thread-buyername']")))
        # time.sleep(3)
        allBuyerNameElements = list.find_elements_by_css_selector("[class*='a-size-small thread-buyername']")
        wait.WebDriverWait(driver, 10000).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[class*='a-size-mini thread-timestamp']")))
        # time.sleep(3)
        allBuyerDate = list.find_elements_by_css_selector("[class*='a-size-mini thread-timestamp']")
        for i, j, d in zip(allLetterTitleElements, allBuyerNameElements, allBuyerDate):
            i.click()
            buyerName = j.text
            buyerDate = d.text
            dateObj = ''
            selectDateObj = datetime.date(year, month, day)
            s = buyerDate.split()
            if ':' in buyerDate:
                dateObj = datetime.date.today()
            else:
                monthDic = {'Jan': 1, 'Feb': 2,
                            'Mar': 3, 'Apr': 4,
                            'May': 5, 'Jun': 6,
                            'Jul': 7, 'Aug': 8,
                            'Sep': 9, 'Oct': 10,
                            'Nov': 11, 'Dec': 12}
                dateObj = datetime.date(datetime.date.today().year, monthDic[s[0]], int(s[1]))

            if dateObj in selectDateObjList:
                wait.WebDriverWait(driver, 10000).until(
                    EC.presence_of_element_located((By.ID, "currentThreadSenderId")))
                currentThreadSenderId = driver.find_element_by_id('currentThreadSenderId').get_attribute('value')
                oriString = i.text
                pattern = re.compile(r'\d*-\d*-\d*')
                str2 = re.findall(pattern, oriString)
                if len(str2) != 0:
                    getId = str2[0]
                    print(currentThreadSenderId, '         ', getId, '     ', buyerName, '      ', buyerDate)
                    sheet.write(n, 0, currentThreadSenderId)
                    sheet.write(n, 1, getId)
                    sheet.write(n, 2, buyerName)
                    sheet.write(n, 3, buyerDate)
                    n = n + 1
            elif dateObj < dateStart:
                stop = True
                break

        if stop == True:
            break
        pageDiv = wait.WebDriverWait(driver, 100000).until(EC.presence_of_element_located((By.ID, 'pagination-box')))
        nextPageButton = pageDiv.find_element_by_xpath(r"//*[contains(text(),'→')]")
        nextPageButtonClass = nextPageButton.get_attribute("class")

        print(nextPageButtonClass)
        if nextPageButtonClass == 'a-disabled a-last':
            break
        else:
            nextPageButton.click()
            # time.sleep(2)
        index = index + 1

    # 最后，将以上操作保存到指定的Excel文件中
    book.save(excelUrl)  # 在字符串前加r，声明为raw字符串，这样就不会处理其中的转义了。否则，可能会报错
    driver.close()
    return

if __name__ == '__main__':
    now = datetime.datetime.now()
    date = now + datetime.timedelta(days=-1)
    # month = date.strftime("%b")
    # day = int(date.strftime("%d"))
    month = date.month
    day = date.day
    # localtime = time.localtime(time.time())
    # if localtime.tm_hour == 0 and localtime.tm_min == 0 and localtime.tm_sec == 0:
    getDatas(2018, month, day)
