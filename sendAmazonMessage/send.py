import traceback
from selenium import webdriver
from selenium.webdriver.chrome import options
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.support import wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import tool
import os.path
from boltons import iterutils
from VAR import bMutex
import re
def generateSendMessageUrl(orderID):
    ori = r'https://sellercentral.amazon.com/gp/help/contact/contact.html?orderID=%s&marketplaceID=ATVPDKIKX0DER'%(orderID)
    return ori
def sendMessage(sendMessageUrl, modelStr, driver,orderid):
    while True:
        try:
            # 选择subject为order Infomation
            print('start to send')
            bMutex.lock()
            driver.get(sendMessageUrl)
            bMutex.unlock()
            time.sleep(2)
            bMutex.lock()
            selectButtonWait = wait.WebDriverWait(driver,100000).until(EC.visibility_of_element_located((By.ID,'commMgrCompositionSubject')))
            selectSubject = Select(driver.find_element_by_id('commMgrCompositionSubject'))
            selectSubject.select_by_index(1)


            # 获取名字
            twoNameDiv = driver.find_elements_by_css_selector("[style='padding-bottom:2px']")
            name = twoNameDiv[0].text.strip()
            p = re.compile(r':(.*)\(')
            t = re.search(p, name)
            name = t.group(1)
            # 获取订单详情
            productname = driver.find_element_by_css_selector("[style='list-style-position:inside; padding-left:0; margin-left:0']").text
            bMutex.unlock()

            if len(productname) > 80:
                productname = tool.getorderinfo2(driver,orderid)

            # 对model进行智能处理
            patternOrderid = re.compile(r'#orderid')
            patternUsername = re.compile(r'#username')
            patternProductname = re.compile(r'#productname')
            modelStr = re.sub(patternOrderid,orderid,modelStr)
            modelStr = re.sub(patternUsername,name,modelStr)
            modelStr = re.sub(patternProductname,productname,modelStr)
            modelStr = '%r'%modelStr
            # 发送的内容
            # modelStr = 'dear '+name+':\n'+modelStr
            bMutex.lock()
            wait.WebDriverWait(driver,100000).until(EC.visibility_of_element_located((By.ID,'commMgrCompositionMessage')))
            textArea = driver.find_element_by_id('commMgrCompositionMessage')
            driver.execute_script("arguments[0].value="+modelStr+";",textArea)
            bMutex.unlock()
            time.sleep(1)

            # chunkModel = iterutils.chunked(modelStr,100)
            # for i in chunkModel:
            #     textArea.send_keys(i)


            # textArea.send_keys(modelStr)

            # 点击发送邮件按钮
            bMutex.lock()
            wait.WebDriverWait(driver,10000).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'#sendemail_label')))
            allSendMailLabel = driver.find_elements_by_css_selector('#sendemail')
            allSendMailLabel = allSendMailLabel[1]
            driver.execute_script("arguments[0].click();", allSendMailLabel)

            # 点了发送休息2S
            # time.sleep(3)
            wait.WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.NAME, 'Back to Manage Orders')))
            bMutex.unlock()
            print('send OK')
            return name
        except Exception as e:
            bMutex.unlock()
            traceback.print_exc()
            print('try send again----------------------')