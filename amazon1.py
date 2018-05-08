from selenium import webdriver
from selenium.webdriver.support import wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import re
import time
basePath = r'C:\Program Files (x86)\Google\Chrome\Application'
path = os.path.join(basePath,'chromedriver.exe')
cOptions = webdriver.ChromeOptions()
cOptions.add_argument(r'user-data-dir=C:\Users\pro\AppData\Local\Google\Chrome\User Data')
driver = webdriver.Chrome(executable_path=path,options=cOptions)
url = r'https://sellercentral.amazon.com/messaging/inbox'
print('ok?')
# web.get()
driver.get(url)
returnAllMessage = wait.WebDriverWait(driver,10000000).until(EC.presence_of_element_located((By.ID,'current-filter-text')))

# returnAllMessage = web.find_element_by_id('current-filter-text')
returnAllMessage.click()

allMessage = driver.find_element_by_link_text('All Messages')
allMessage.click()

wait.WebDriverWait(driver,10000).until(EC.presence_of_element_located((By.ID,'threads-list')))
list = driver.find_element_by_id('threads-list')
allLetterTitleElements = list.find_elements_by_css_selector("[class*='a-size-small thread-subject']")
allBuyerNameElements = list.find_elements_by_css_selector("[class*='a-size-small thread-buyername']")
for i,j in zip(allLetterTitleElements,allBuyerNameElements):
    i.click()
    buyerName = j.text
    currentThreadSenderID = driver.find_element_by_id('currentThreadSenderId').get_attribute('value')
    oriString = i.text
    pattern = re.compile(r'\d*-\d*-\d*')
    str = re.findall(pattern,oriString)
    if len(str)!=0:
        getID = str[0]
        print(currentThreadSenderID,'         ',getID,'     ',buyerName)
time.sleep(100)