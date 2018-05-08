# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support import wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import re
import time
import xlwt

basePath = r'C:\Program Files (x86)\Google\Chrome\Application'

path = os.path.join(basePath, 'chromedriver.exe')
cOptions = webdriver.ChromeOptions()
cOptions.add_argument(r'user-data-dir=C:\Users\pro\AppData\Local\Google\Chrome\User Data')
driver = webdriver.Chrome(executable_path=path, options=cOptions)

# driver = webdriver.Chrome('/Users/djc/Downloads/chromedriver')
url = r'https://sellercentral.amazon.com/messaging/inbox'
# url = r'file:///Users/djc/Downloads/Amazon.html'
# excelUrl = r'/Users/djc/Desktop/test1.xls'
excelUrl = os.path.join('.', 'result.xls')
print('ok?')

# web.get()
driver.get(url)
returnAllMessage = wait.WebDriverWait(driver, 10000000).until(
    EC.presence_of_element_located((By.ID, 'current-filter-text')))

# returnAllMessage = web.find_element_by_id('current-filter-text')
returnAllMessage.click()

allMessage = wait.WebDriverWait(driver, 10000000).until(EC.presence_of_element_located((By.LINK_TEXT, 'All Messages')))
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
while True:
    time.sleep(2)
    wait.WebDriverWait(driver, 10000).until(EC.visibility_of_element_located((By.ID, 'threads-list')))
    list = driver.find_element_by_id('threads-list')
    # time.sleep(2)
    # EC.visibility_of
    t1 = wait.WebDriverWait(driver,10000).until(EC.presence_of_element_located((By.CSS_SELECTOR,"[class*='a-size-small thread-subject']")))
    print(t1.text)
    # time.sleep(3)
    allLetterTitleElements = list.find_elements_by_css_selector("[class*='a-size-small thread-subject']")
    wait.WebDriverWait(driver,10000).until(EC.presence_of_element_located((By.CSS_SELECTOR,"[class*='a-size-small thread-buyername']")))
    # time.sleep(3)
    allBuyerNameElements = list.find_elements_by_css_selector("[class*='a-size-small thread-buyername']")
    wait.WebDriverWait(driver,10000).until(EC.presence_of_element_located((By.CSS_SELECTOR,"[class*='a-size-mini thread-timestamp']")))
    # time.sleep(3)
    allBuyerDate = list.find_elements_by_css_selector("[class*='a-size-mini thread-timestamp']")
    for i, j, d in zip(allLetterTitleElements, allBuyerNameElements, allBuyerDate):
        i.click()
        buyerName = j.text
        buyerDate = d.text
        wait.WebDriverWait(driver, 10000).until(
            EC.presence_of_element_located((By.ID,"currentThreadSenderId")))
        currentThreadSenderId = driver.find_element_by_id('currentThreadSenderId').get_attribute('value')
        oriString = i.text
        pattern = re.compile(r'\d*-\d*-\d*')
        str = re.findall(pattern, oriString)
        if len(str) != 0:
            getId = str[0]
            print(currentThreadSenderId, '         ', getId, '     ', buyerName, '      ', buyerDate)
            sheet.write(n, 0, currentThreadSenderId)
            sheet.write(n, 1, getId)
            sheet.write(n, 2, buyerName)
            sheet.write(n, 3, buyerDate)
            n = n + 1
    pageDiv = wait.WebDriverWait(driver, 100000).until(EC.presence_of_element_located((By.ID, 'pagination-box')))
    nextPageButton = pageDiv.find_element_by_xpath(r"//*[contains(text(),'→')]")
    nextPageButtonClass = nextPageButton.get_attribute("class")
    print(nextPageButtonClass)
    if nextPageButtonClass == 'a-disabled a-last':
        break
    else:
        nextPageButton.click()
        # time.sleep(2)
    index = index+1
    # if index == 4:
    #     book.save(excelUrl)  # 在字符串前加r，声明为raw字符串，这样就不会处理其中的转义了。否则，可能会报错
    #     break

# 最后，将以上操作保存到指定的Excel文件中
book.save(excelUrl)  # 在字符串前加r，声明为raw字符串，这样就不会处理其中的转义了。否则，可能会报错
# time.sleep(100000)
