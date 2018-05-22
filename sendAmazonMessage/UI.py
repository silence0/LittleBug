from PyQt5 import QtWidgets
from PyQt5 import QtCore
import sys
import send
import tool
import os
from selenium import webdriver
from selenium.webdriver.chrome import options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import getpass
from boltons import iterutils


class mySingal(QtCore.QObject):
    graySignal = QtCore.pyqtSignal()
    ungraySignal = QtCore.pyqtSignal()
    informationSignao = QtCore.pyqtSignal(str, str)



class sendByDateClickedThread(QtCore.QThread):
    def __init__(self, mainWindow):
        super(sendByDateClickedThread, self).__init__()
        self.window = mainWindow
        self.singals = mySingal()

    def run(self):
        self.singals.graySignal.emit()

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
        self.singals.informationSignao.emit('information', 'completed successfully')
        self.singals.ungraySignal.emit()


class sendByIDClickedThread(QtCore.QThread):
    def __init__(self, mainwindow):
        super(sendByIDClickedThread, self).__init__()
        self.window = mainwindow
        self.singals = mySingal()

    def run(self):
        # self.window.grayAllButton()
        self.singals.graySignal.emit()
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
        # QtWidgets.QMessageBox().information(self.window, 'information',
        #                                     'send by ID has been completed',
        #                                     QtWidgets.QMessageBox.Ok)
        self.singals.informationSignao.emit('information', 'completed successfully')
        self.singals.ungraySignal.emit()


class searchClickedThread(QtCore.QThread):
    def __init__(self, mainwindow):
        super(searchClickedThread, self).__init__()
        self.window = mainwindow
        self.singals = mySingal()

    def run(self):
        self.singals.graySignal.emit()
        self.window.modelText = self.window.modelInput.toPlainText()
        self.window.driver = webdriver.Chrome(executable_path=self.window.driverPath, options=self.window.chromeOptions)
        self.window.driver.get(self.window.selectDateUrl)
        time.sleep(3)
        self.window.orderList, self.window.dateList,self.orderNameList = tool.getlist(self.window.driver)
        print('test result:',self.orderNameList)
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
        # self.window.searchCompleteInfomation = QtWidgets.QMessageBox().information(self.window, 'infomation',
        #                                                                            'search has been completed,and table saved',
        #                                                                            QtWidgets.QMessageBox.Ok)
        # self.window.ungrayAllButton()
        self.singals.informationSignao.emit('information', 'completed successfully')
        self.singals.ungraySignal.emit()


class MyMainWindow(QtWidgets.QScrollArea):
    def __init__(self):
        super(MyMainWindow, self).__init__()
        self.modelInput = QtWidgets.QTextEdit()
        self.sendByDate = QtWidgets.QPushButton('sendByDate')
        self.sendByID = QtWidgets.QPushButton('sendByID')
        self.searchAllID = QtWidgets.QPushButton('search')
        self.modelInputGuid = QtWidgets.QLabel('Message template:')
        self.IDInputGuid = QtWidgets.QLabel('Please input the ID list you want to send message:')
        self.IDInput = QtWidgets.QTextEdit()
        self.nameList = []

        self.driverBasePath = r'C:\Program Files (x86)\Google\Chrome\Application'
        # self.driverBasePath = r'D:\userdata'
        self.driverPath = os.path.join(self.driverBasePath, 'bindriver.exe')

        userDatePath = r'C:\Users\%s\AppData\Local\Google\Chrome\User Data' % (getpass.getuser())

        # userDatePath = r'D:\userdata'
        self.chromeOptions = webdriver.ChromeOptions()
        self.chromeOptions.add_argument(r'user-data-dir=' + userDatePath)

        # self.sendMessageUrl = r'file:///C:/Users/60913/Desktop/4_files/6.html'
        self.selectDateUrl = r'https://sellercentral.amazon.com/gp/orders-v2/search/ref=ag_myosearch_apsearch_myo'
        # self.getOrderListUrl = r'file:///C:/Users/60913/Desktop/4_files/2.html'
        self.getThreadUrl = r'https://sellercentral.amazon.com/messaging/inbox/ref=ag_cmin_head_xx'
        # self.driver = webdriver.Chrome(executable_path=driverPath, options=chromeOptions)

        self.myLayout = QtWidgets.QVBoxLayout()
        self.myLayout.addWidget(self.modelInputGuid)
        self.myLayout.addWidget(self.modelInput)
        self.myLayout.addWidget(self.IDInputGuid)
        self.myLayout.addWidget(self.IDInput)
        self.myLayout.addWidget(self.sendByDate)
        self.myLayout.addWidget(self.sendByID)
        self.myLayout.addWidget(self.searchAllID)
        self.setLayout(self.myLayout)
        self.resize(400, 500)

        self.sendByDate.clicked.connect(self.sendByDateClicked)
        self.sendByID.clicked.connect(self.sendByIDClicked)
        self.searchAllID.clicked.connect(self.searchClicked)

    def graySlot(self):
        self.sendByID.setEnabled(False)
        self.sendByDate.setEnabled(False)
        self.searchAllID.setEnabled(False)

    def ungraySlot(self):
        self.sendByID.setEnabled(True)
        self.sendByDate.setEnabled(True)
        self.searchAllID.setEnabled(True)

    def informationSlot(self, title, message):
        QtWidgets.QMessageBox().information(self, title, message, QtWidgets.QMessageBox.Ok)

    def sendByDateClicked(self):
        self.th1 = sendByDateClickedThread(self)
        self.th1.singals.graySignal.connect(self.graySlot)
        self.th1.singals.ungraySignal.connect(self.ungraySlot)
        self.th1.singals.informationSignao.connect(self.informationSlot)
        self.th1.start()

    def sendByIDClicked(self):
        self.th2 = sendByIDClickedThread(self)
        self.th2.singals.graySignal.connect(self.graySlot)
        self.th2.singals.ungraySignal.connect(self.ungraySlot)
        self.th2.singals.informationSignao.connect(self.informationSlot)
        self.th2.start()

    def searchClicked(self):
        self.th3 = searchClickedThread(self)
        self.th3.singals.graySignal.connect(self.graySlot)
        self.th3.singals.ungraySignal.connect(self.ungraySlot)
        self.th3.singals.informationSignao.connect(self.informationSlot)
        self.th3.start()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    t = MyMainWindow()
    t.show()
    app.exec_()
