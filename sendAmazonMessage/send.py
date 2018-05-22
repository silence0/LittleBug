import traceback
from selenium import webdriver
from selenium.webdriver.chrome import options
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.support import wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import os.path
from boltons import iterutils

import re
def generateSendMessageUrl(orderID):
    ori = r'https://sellercentral.amazon.com/gp/help/contact/contact.html?orderID=%s&marketplaceID=ATVPDKIKX0DER'%(orderID)
    return ori
def sendMessage(sendMessageUrl, modelStr, driver,orderid):
    while True:
        try:
            # 选择subject为order Infomation
            print('start to send again')
            driver.get(sendMessageUrl)
            time.sleep(2)
            selectButtonWait = wait.WebDriverWait(driver,100000).until(EC.visibility_of_element_located((By.ID,'commMgrCompositionSubject')))
            selectSubject = Select(driver.find_element_by_id('commMgrCompositionSubject'))
            selectSubject.select_by_index(1)


            # 获取名字
            twoNameDiv = driver.find_elements_by_css_selector("[style='padding-bottom:2px']")
            name = twoNameDiv[0].text.strip()
            p = re.compile(r':(.*)\(')
            t = re.search(p, name)
            name = t.group(1)

            # 对model进行智能处理
            patternOrderid = re.compile(r'#orderid')
            patternUsername = re.compile(r'#username')
            modelStr = re.sub(patternOrderid,orderid,modelStr)
            modelStr = re.sub(patternUsername,name,modelStr)

            # 发送的内容
            # modelStr = 'dear '+name+':\n'+modelStr
            wait.WebDriverWait(driver,100000).until(EC.visibility_of_element_located((By.ID,'commMgrCompositionMessage')))
            textArea = driver.find_element_by_id('commMgrCompositionMessage')
            chunkModel = iterutils.chunked(modelStr,100)
            for i in chunkModel:
                textArea.send_keys(i)

            # textArea.send_keys(modelStr)

            # 点击发送邮件按钮
            wait.WebDriverWait(driver,10000).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'#sendemail_label')))
            allSendMailLabel = driver.find_elements_by_css_selector('#sendemail_label')
            for i in allSendMailLabel:
                try:
                    i.click()
                except:
                    pass
            # 点了发送休息2S
            time.sleep(3)
            print('send OK')
            return name
        except Exception as e:
            traceback.print_exc()