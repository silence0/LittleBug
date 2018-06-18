import time

from PyQt5 import QtCore
from selenium import webdriver
import send
import tool
import traceback
from VAR import bMutex
# Qt的信号，用于工作线程和GUI线程间的交互
class mySingal(QtCore.QObject):
    graySignal = QtCore.pyqtSignal()
    ungraySignal = QtCore.pyqtSignal()
    getOrderIDListCompletedSignal = QtCore.pyqtSignal()
    errorSignal = QtCore.pyqtSignal()
    informationSignal = QtCore.pyqtSignal(str, str)
    scheduleSignal = QtCore.pyqtSignal(str)
    addLogItemSignal = QtCore.pyqtSignal(str)

# 按照日期发送信件——工作线程
class sendByDateClickedThread(QtCore.QThread):
    def __init__(self, mainWindow):
        super(sendByDateClickedThread, self).__init__(mainWindow)
        self.window = mainWindow

    def run(self):
        try:
            bMutex.lock()
            self.window.driver = webdriver.Firefox(executable_path=self.window.driverPath,firefox_profile=self.window.profile)
            self.window.setDriver(self.window.driver)
            self.window.modelText = self.window.getModelInputWidget().toPlainText()
            # 先把之前生成的发送情况给清除掉
            t = open('allID.txt', 'w')
            t.close()
            t = open('sendID.txt', 'w')
            t.close()


            # 获取orderid,并创建各种list
            self.window.driver.get(self.window.selectDateUrl)
            bMutex.unlock()
            self.window.orderList, self.window.dateList = tool.getlist(self.window.driver)
            self.window.currentThreadSenderList = []
            self.window.nameList = []

            # 将allID写入
            for i in self.window.orderList:
                allID = open('allID.txt', 'a+')
                allID.write(i + '\n')
                allID.close()
            orderSizeStr = str(len(self.window.orderList))
            self.window.s.scheduleSignal.emit(str(0)+r'/'+orderSizeStr)
            completedIndex = 0
            for i in self.window.orderList:
                sendUrl = send.generateSendMessageUrl(i)
                thisName = send.sendMessage(sendUrl, self.window.modelText, self.window.driver, i)
                self.window.nameList.append(thisName)
                haveSentID = open('sendID.txt', 'a+')
                haveSentID.write(i + '\n')
                haveSentID.close()
                completedIndex = completedIndex+1

                self.window.s.addLogItemSignal.emit('Order ID:'+str(i)+'\nUser Name'+thisName)
                self.window.s.scheduleSignal.emit(str(completedIndex)+r'/'+orderSizeStr)
            self.window.driver.close()
            self.window.s.informationSignal.emit('information', 'completed successfully')
            self.window.s.ungraySignal.emit()
        except Exception as e:
            bMutex.unlock()
            traceback.print_exc()
            self.window.s.errorSignal.emit()

# 按照ID发送信件——工作线程
class sendByIDClickedThread(QtCore.QThread):
    def __init__(self, mainwindow):
        super(sendByIDClickedThread, self).__init__(mainwindow)
        self.window = mainwindow

    def run(self):
        try:
            bMutex.lock()
            self.window.driver = webdriver.Firefox(executable_path=self.window.driverPath,firefox_profile=self.window.profile)
            self.window.setDriver(self.window.driver)
            bMutex.unlock()
            time.sleep(60)
            self.window.modelText = self.window.getModelInputWidget().toPlainText()
            self.window.nameList = []
            allID = self.window.getIDInputWidget().toPlainText()
            allIDList = allID.split('\n')
            # 先把之前生成的发送情况给清除掉
            t = open('allID.txt', 'w')
            t.close()
            t = open('sendID.txt', 'w')
            t.close()
            for i in allIDList:
                if i == '':
                    continue
                f = open('allID.txt', 'a+')
                f.write(i + '\n')
                f.close()
            orderSizeStr = str(len(allIDList))
            self.window.s.scheduleSignal.emit(str(0) + r'/' + orderSizeStr)
            completedIndex = 0
            for i in allIDList:
                if i == '':
                    continue
                sendUrl = send.generateSendMessageUrl(i)
                thisName = send.sendMessage(sendUrl, self.window.modelText, self.window.driver, i)
                self.window.nameList.append(thisName)
                haveSentID = open('sendID.txt', 'a+')
                haveSentID.write(i + '\n')
                haveSentID.close()
                completedIndex = completedIndex+1

                self.window.s.addLogItemSignal.emit('Order ID:'+str(i)+'\nUser Name'+thisName)
                self.window.s.scheduleSignal.emit(str(completedIndex)+r'/'+orderSizeStr)

            self.window.driver.close()
            self.window.s.informationSignal.emit('information', 'completed successfully')
            self.window.s.ungraySignal.emit()
        except Exception as e:
            bMutex.unlock()
            traceback.print_exc()
            self.window.s.errorSignal.emit()

# 搜索并生成表格——工作线程
class searchClickedThread(QtCore.QThread):
    def __init__(self, mainwindow):
        super(searchClickedThread, self).__init__(parent=mainwindow)
        self.window = mainwindow

    def run(self):
        try:
            bMutex.lock()
            self.window.modelText = self.window.getModelInputWidget().toPlainText()
            self.window.driver = webdriver.Firefox(executable_path=self.window.driverPath,firefox_profile=self.window.profile)
            self.window.setDriver(self.window.driver)
            self.window.driver.get(self.window.selectDateUrl)
            bMutex.unlock()
            time.sleep(3)
            self.window.orderList, self.window.dateList = tool.getlist(self.window.driver)
            self.window.currentThreadSenderList = []
            self.window.nameList = []
            orderSizeStr = str(len(self.window.orderList))
            self.window.s.scheduleSignal.emit(str(0) + r'/' + orderSizeStr)
            completedIndex = 0
            #         拿这些ID去搜索
            bMutex.lock()
            self.window.driver.get(self.window.getThreadUrl)
            bMutex.unlock()
            time.sleep(3)
            lastCurrent = 0
            lastOrder = 0
            abnormalID = []
            for i in self.window.orderList:
                while True:
                    get = tool.getcurrent2(self.window.driver, i,lastcurrentid=lastCurrent,lastorderid=lastOrder)
                    if get == None:
                        #                 说明没搜索到，那么就要给他发信
                        send.sendMessage2(send.generateSendMessageUrl(i), self.window.modelText, self.window.driver, i)
                    elif get == 'abnormal':
                        self.window.currentThreadSenderList.append('unknown')
                        abnormalID.append(i)
                        lastOrder = i
                        lastCurrent = get
                        break
                    else:
                        #                     说明搜索到了，那么这个信件就不用重新发了
                        self.window.currentThreadSenderList.append(get)
                        lastOrder = i
                        lastCurrent = get
                        break

                self.window.s.addLogItemSignal.emit('Order ID:' + str(i) + '\nCurrentThreadSenderID:' + str(get))
                completedIndex = completedIndex + 1
                self.window.s.scheduleSignal.emit(str(completedIndex) + r'/' + orderSizeStr)

            tool.writeExcelAndAbnormalId(self.window.currentThreadSenderList, self.window.orderList, self.window.dateList, abnormalID)
            self.window.driver.close()

            self.window.s.informationSignal.emit('information', 'completed successfully')
            self.window.s.ungraySignal.emit()
        except Exception as e:
            bMutex.unlock()
            traceback.print_exc()
            self.window.s.errorSignal.emit()
