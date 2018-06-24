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
# 用于生成，给特定的人发送信件时需要打开的网页地址
# 发信的网址
def generateSendMessageUrl(orderID):
    ori = r'https://sellercentral.amazon.com/gp/help/contact/contact.html?orderID=%s&marketplaceID=ATVPDKIKX0DER'%(orderID)
    return ori
# 不使用标签进行发信(在单纯使用发信功能时调用,因为从始至终只需要在一个页面内)
def sendMessage(sendMessageUrl, modelStr, driver,orderid):
    # 循环的目的是为了在发生未知错误时,能够重新进行一次
    while True:
        try:
            # 选择subject为order Infomation
            print('start to send')
            bMutex.lock()
            driver.get(sendMessageUrl)
            bMutex.unlock()
            time.sleep(2)
            bMutex.lock()
            selectButtonWait = wait.WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.ID,'commMgrCompositionSubject')))
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
            wait.WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.ID,'commMgrCompositionMessage')))
            textArea = driver.find_element_by_id('commMgrCompositionMessage')
            driver.execute_script("arguments[0].value="+modelStr+";",textArea)
            bMutex.unlock()
            time.sleep(1)


            # 点击发送邮件按钮
            bMutex.lock()
            wait.WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'#sendemail_label')))
            allSendMailLabel = driver.find_elements_by_css_selector('#sendemail')
            allSendMailLabel = allSendMailLabel[1]
            driver.execute_script("arguments[0].click();", allSendMailLabel)

            # 点了发送休息2S
            # time.sleep(3)
            wait.WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'Back to Manage Orders')))
            bMutex.unlock()
            print('send OK')
            return name
        except Exception as e:
            bMutex.unlock()
            traceback.print_exc()
            print('try send again----------------------')

# 使用标签来进行发信(在使用搜索功能时,为了提高速度,查找信件的那个页面不关闭,故在新标签内发信)
def sendMessage2(sendMessageUrl, modelStr, driver,orderid):
    while True:
        try:
            # 选择subject为order Infomation
            print('start to send')
            bMutex.lock()
            # driver.get(sendMessageUrl)
            js = 'window.open(\"' + sendMessageUrl + '\");'
            handle = driver.current_window_handle
            driver.execute_script(js)

            handles = driver.window_handles
            for newhandle in handles:

                # 筛选新打开的窗口B

                if newhandle != handle:
                    # 切换到新打开的窗口B

                    driver.switch_to_window(newhandle)

            # 在新打开的窗口B中操作

            bMutex.unlock()
            time.sleep(2)
            bMutex.lock()
            selectButtonWait = wait.WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.ID,'commMgrCompositionSubject')))
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
                productname = tool.getorderinfo3(driver,orderid)

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
            wait.WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.ID,'commMgrCompositionMessage')))
            textArea = driver.find_element_by_id('commMgrCompositionMessage')
            driver.execute_script("arguments[0].value="+modelStr+";",textArea)
            bMutex.unlock()
            time.sleep(1)


            # 点击发送邮件按钮
            bMutex.lock()
            wait.WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'#sendemail_label')))
            allSendMailLabel = driver.find_elements_by_css_selector('#sendemail')
            allSendMailLabel = allSendMailLabel[1]
            driver.execute_script("arguments[0].click();", allSendMailLabel)

            # 点了发送休息2S
            # time.sleep(3)
            wait.WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'Back to Manage Orders')))

            # 关闭当前窗口B

            driver.close()

            # 切换回窗口A

            driver.switch_to_window(handles[0])

            bMutex.unlock()
            print('send OK')
            return name
        except Exception as e:
            # 关闭当前窗口B

            driver.close()

            # 切换回窗口A

            driver.switch_to_window(handles[0])
            bMutex.unlock()
            traceback.print_exc()
            print('try send again----------------------')
