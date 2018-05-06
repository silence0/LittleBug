from selenium import webdriver
from selenium.webdriver.support import wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import os.path,time
basePath = r'C:\Program Files (x86)\Google\Chrome\Application'
path = os.path.join(basePath,'chromedriver.exe')
print(path)

driverOptions = webdriver.ChromeOptions()
driverOptions.add_argument(r'user-data-dir=C:\Users\60913\AppData\Local\Google\Chrome\User Data')
driver = webdriver.Chrome(options=driverOptions,executable_path=path)
print("what???")
t = driver.get(r"https://github.com/Lyanf")
driver.close()
print('wait')
title = 'Katana Framework武士刀操作指南'
# waitA = wait.WebDriverWait(driver,10).until(EC.visibility_of((By.ID,r'img_out_609136080')))
# print(driver.page_source)
# print('here')
# driver.get(r'http://www.hao123.com/')
# driver.implicitly_wait(10)
# time.sleep(10)
link  = wait.WebDriverWait(driver,10000).until(EC.presence_of_element_located((By.ID,'folder_1')))
time.sleep(1)
# driver.find_element_by_css_selector("a[title='Katana Framework武士刀操作指南'").click()
link.click()
driver.switch_to.frame('mainFrame')
# time.sleep(5)
t  = wait.WebDriverWait(driver,10000).until(EC.text_to_be_present_in_element((By.TAG_NAME,'u'),'yanfeng，在线收款从未如此简单！'))
print('get!')
# print(driver.page_source)
# link2 = driver.find_elements_by_class_name('no')
# print(link2)
# for i in link2:
#     print(i)
# link2[0].click()
# li('img_out_609136080').click()
link2 = driver.find_element_by_css_selector("u[tabindex='0'")
print(type(link2))
link2.click()
print(t)
time.sleep(3)