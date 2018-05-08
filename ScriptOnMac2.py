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

# basePath = r'C:\Program Files (x86)\Google\Chrome\Application'
# path = os.path.join(basePath,'chromedriver.exe')
# cOptions = webdriver.ChromeOptions()
# cOptions.add_argument(r'user-data-dir=C:\Users\pro\AppData\Local\Google\Chrome\User Data')
# driver = webdriver.Chrome(executable_path=path,options=cOptions)


def getDatas(month,day):
    driver = webdriver.Chrome('/Users/djc/Downloads/chromedriver')
    # url = r'https://sellercentral.amazon.com/messaging/inbox'
    url = r'file:///Users/djc/Downloads/Amazon.html'
    excelUrl = r'/Users/djc/Desktop/'+ month + '_'+ day + '.xls'
    print('ok?')


    # web.get()
    driver.get(url)
    returnAllMessage = wait.WebDriverWait(driver,10000000).until(EC.presence_of_element_located((By.ID,'current-filter-text')))

    # returnAllMessage = web.find_element_by_id('current-filter-text')
    # returnAllMessage.click()

    allMessage = driver.find_element_by_link_text('All Messages')
    # allMessage.click()

    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('test', cell_overwrite_ok=True)
    sheet.write(0, 0, 'currentThreadSenderId')  
    sheet.write(0, 1, 'orderId')
    sheet.write(0, 2, 'buyerName')

    wait.WebDriverWait(driver,10000).until(EC.presence_of_element_located((By.ID,'threads-list')))
    list = driver.find_element_by_id('threads-list')
    allLetterTitleElements = list.find_elements_by_css_selector("[class*='a-size-small thread-subject']")
    allBuyerNameElements = list.find_elements_by_css_selector("[class*='a-size-small thread-buyername']")
    allBuyerDate = list.find_elements_by_css_selector("[class*='a-size-mini thread-timestamp']")

    n = 1

    for i,j,d in zip(allLetterTitleElements,allBuyerNameElements,allBuyerDate):
        i.click()
        buyerName = j.text
        buyerDate = d.text

        s = buyerDate.split()
        if str[0] == month and int(str[1]) == day:
            currentThreadSenderId = driver.find_element_by_id('currentThreadSenderId').get_attribute('value')
            oriString = i.text
            pattern = re.compile(r'\d*-\d*-\d*')
            str = re.findall(pattern,oriString)
            if len(str)!=0:
                getId = str[0]
                print(currentThreadSenderId,'         ',getId,'     ',buyerName,'      ',buyerDate)
                sheet.write(n,0,currentThreadSenderId)
                sheet.write(n,1,getId)
                sheet.write(n,2,buyerName)
                n+=1

        elif n>4:
            break
    # 最后，将以上操作保存到指定的Excel文件中
    book.save(excelUrl)

    driver.close()

    return



while True:
    now = datetime.datetime.now()
    date = now + datetime.timedelta(days = -1)
    month = date.strftime("%b")
    day = int(date.strftime("%d"))

    localtime = time.localtime(time.time())
    if localtime.tm_hour == 0 and localtime.tm_min == 0 and localtime.tm_sec == 0:
        getDatas(month,day)

       


