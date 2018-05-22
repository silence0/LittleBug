import time

from PyQt5 import QtCore
from selenium import webdriver

import send
import tool


class mySingal(QtCore.QObject):
    graySignal = QtCore.pyqtSignal()
    ungraySignal = QtCore.pyqtSignal()
    informationSignal = QtCore.pyqtSignal(str, str)
    scheduleSignal = QtCore.pyqtSignal(str)
    addLogItemSignal = QtCore.pyqtSignal(str)

class testThread(QtCore.QThread):
    def __init__(self,mainWindow):
        super(testThread, self).__init__()
        self.mainWindow = mainWindow
    def run(self):
        print('run@')
        # self.mainWindow.s.graySignal.emit()
        self.mainWindow.s.ungraySignal.emit()
class sendByDateClickedThread(QtCore.QThread):
    def __init__(self, mainWindow):
        super(sendByDateClickedThread, self).__init__()
        self.window = mainWindow

    def run(self):

        self.window.driver = webdriver.Chrome(executable_path=self.window.driverPath, options=self.window.chromeOptions)
        self.window.modelText = self.window.modelInput.toPlainText()
        # 先把之前生成的发送情况给清除掉
        t = open('allID.txt', 'w')
        t.close()
        t = open('sendID.txt', 'w')
        t.close()

        # 先让人选日期
        self.window.driver.get(self.window.selectDateUrl)

        # 获取orderid,并创建各种list
        self.window.driver.get(self.window.selectDateUrl)
        self.window.orderList, self.window.dateList = tool.getlist(self.window.driver)
        self.window.currentThreadSenderList = []
        self.window.nameList = []

        # 将allID写入
        for i in self.window.orderList:
            allID = open('allID.txt', 'a+')
            allID.write(i + '\n')
            allID.close()

        # 发信
        # 每发一封信，必须要保存已经发送信件的人的id，以达到终止后能够继续的效果
        for i in self.window.orderList:
            sendUrl = send.generateSendMessageUrl(i)
            thisName = send.sendMessage(sendUrl, self.window.modelText, self.window.driver, i)
            self.window.nameList.append(thisName)
            haveSentID = open('sendID.txt', 'a+')
            haveSentID.write(i + '\n')
            haveSentID.close()
        self.window.driver.close()
        # QtWidgets.QMessageBox().information(self.window, 'information',
        #                                     'send by date has been completed', QtWidgets.QMessageBox.Ok)
        self.parent().s.informationSignal.emit('information', 'completed successfully')
        self.parent().s.ungraySignal.emit()


class sendByIDClickedThread(QtCore.QThread):
    def __init__(self, mainwindow):
        super(sendByIDClickedThread, self).__init__()
        self.window = mainwindow

    def run(self):
        self.window.driver = webdriver.Chrome(executable_path=self.window.driverPath, options=self.window.chromeOptions)
        self.window.modelText = self.window.modelInput.toPlainText()
        self.window.nameList = []
        allID = self.window.IDInput.toPlainText()
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
        for i in allIDList:
            if i == '':
                continue
            sendUrl = send.generateSendMessageUrl(i)
            thisName = send.sendMessage(sendUrl, self.window.modelText, self.window.driver, i)
            self.window.nameList.append(thisName)
            haveSentID = open('sendID.txt', 'a+')
            haveSentID.write(i + '\n')
            haveSentID.close()

        self.window.driver.close()
        self.parent().s.informationSignal.emit('information', 'completed successfully')
        self.parent().s.ungraySignal.emit()


class searchClickedThread(QtCore.QThread):
    def __init__(self, mainwindow):
        super(searchClickedThread, self).__init__()
        self.window = mainwindow

    def run(self):
        self.window.modelText = self.window.modelInput.toPlainText()
        self.window.driver = webdriver.Chrome(executable_path=self.window.driverPath, options=self.window.chromeOptions)
        self.window.driver.get(self.window.selectDateUrl)
        time.sleep(3)
        self.window.orderList, self.window.dateList = tool.getlist(self.window.driver)
        self.window.currentThreadSenderList = []
        self.window.nameList = []

        #         拿这些ID去搜索
        self.window.driver.get(self.window.getThreadUrl)
        time.sleep(3)
        for i in self.window.orderList:
            while True:
                get = tool.getcurrent(self.window.driver, i)
                if get == None:
                    #                 说明没搜索到呀，那么就要给他发信
                    send.sendMessage(send.generateSendMessageUrl(i), self.window.modelText, self.window.driver, i)
                    self.window.driver.get(self.window.getThreadUrl)
                else:
                    #                     说明搜索到了，那么这个信件就不用重新发了
                    self.window.currentThreadSenderList.append(get)
                    break

        tool.writeExcel(self.window.currentThreadSenderList, self.window.orderList, self.window.dateList)
        self.window.driver.close()

        self.parent().s.informationSignal.emit('information', 'completed successfully')
        self.parent().s.singals.ungraySignal.emit()