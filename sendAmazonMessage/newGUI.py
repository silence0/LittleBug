import getpass
import traceback
import os
import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from selenium import webdriver

from MyThread import searchClickedThread, sendByIDClickedThread, sendByDateClickedThread, mySingal,testThread


class Header(QFrame):
    def __init__(self, parent):
        super(Header, self).__init__(parent)
        self.setParent(parent)
        self.parent = parent
        self.initUI()
        self.initStyle()
        self.initConnect()

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.titleLabel = QLabel('Spider')
        self.miniBUtton = QPushButton('-')
        self.closeButton = QPushButton('×')

        self.mainLayout = QHBoxLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mainLayout)

        self.mainLayout.addSpacing(20)
        self.mainLayout.addWidget(self.titleLabel)
        self.mainLayout.addStretch()
        # self.mainLayout.addSpacing(300)
        self.mainLayout.addWidget(self.miniBUtton)
        # self.mainLayout.addSpacing(20)
        self.mainLayout.addWidget(self.closeButton)

    def initStyle(self):
        self.setStyleSheet('''*{background-color:#0081ff;
                            color:white}''')

    def initConnect(self):
        self.miniBUtton.clicked.connect(self.parentWidget().showMinimized)
        self.closeButton.clicked.connect(self.parentWidget().close)

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.parent.m_drag = True
            self.parent.m_DragPosition = event.globalPos() - self.parent.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        try:
            if event.buttons() and Qt.LeftButton:
                self.parent.move(event.globalPos() - self.parent.m_DragPosition)
                event.accept()
        except AttributeError:
            pass

    def mouseReleaseEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.m_drag = False


class MyMainWindow(QFrame):
    def __init__(self):
        super(MyMainWindow, self).__init__()
        self.initUI()
        self.initStyle()
        self.s = mySingal()
        self.initAsySignal()
        self.initPath()

    def initUI(self):
        # self.resize(500,500)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.header = Header(self)
        self.leftFrame = LeftPage(self)
        self.rightFrame = RightPage(self)
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        self.setLayout(self.mainLayout)
        self.twoPage = QHBoxLayout()
        self.twoPage.setSpacing(0)
        self.twoPage.setContentsMargins(0, 0, 0, 0)

        self.mainLayout.addWidget(self.header)
        self.twoPage.addWidget(self.leftFrame)
        self.twoPage.addWidget(self.rightFrame)
        self.mainLayout.addLayout(self.twoPage)

        self.rightFrame.scheduleLabel.setText('')
    def initStyle(self):
        pass

    def initAsySignal(self):
        self.s.graySignal.connect(self.graySlot)
        self.s.ungraySignal.connect(self.ungraySlot)
        self.s.informationSignal.connect(self.informationSlot)
        self.s.errorSignal.connect(self.errorSlot)
        self.s.scheduleSignal.connect(self.scheduleSlot)
        self.s.addLogItemSignal.connect(self.addLogItemSlot)
    def scheduleSlot(self,a):
        self.rightFrame.scheduleLabel.setText(a)
    def informationSlot(self,a,b):
        QMessageBox().information(self,a,b,QMessageBox.Ok)
    def graySlot(self):
        self.leftFrame.startButton.setEnabled(False)
    def ungraySlot(self):
        self.leftFrame.startButton.setEnabled(True)
    def errorSlot(self):
        QMessageBox().information(self,'error','closed by accident!',QMessageBox.Ok)
        self.s.ungraySignal.emit()
    def addLogItemSlot(self,a):
        self.rightFrame.logEdit.setText(a)
    def initPath(self):
        self.driverBasePath = r'C:\Program Files (x86)\Mozilla Firefox'
        # self.driverBasePath = r'D:\userdata'
        self.driverPath = os.path.join(self.driverBasePath, 'geckodriver.exe')

        # userDatePath = r'C:\Users\%s\AppData\Local\Google\Chrome\User Data' % (getpass.getuser())
        lastUserDataPath = r'C:\Users\%s\AppData\Local\Mozilla\Firefox\Profiles'%getpass.getuser()
        t = os.listdir(lastUserDataPath)
        fileName = t[0]
        userDatePath = os.path.join(lastUserDataPath,fileName)
        self.firefoxProfile = webdriver.FirefoxProfile(userDatePath)

        self.selectDateUrl = r'https://sellercentral.amazon.com/gp/orders-v2/search/ref=ag_myosearch_apsearch_myo'
        self.getThreadUrl = r'https://sellercentral.amazon.com/messaging/inbox/ref=ag_cmin_head_xx'

    def getModelInputWidget(self):
        return self.leftFrame.templateInput
    def getIDInputWidget(self):
        return self.leftFrame.IDInput
class LeftPage(QFrame):
    def __init__(self, parent):
        super(LeftPage, self).__init__(parent)
        self.setParent(parent)
        self.parent = parent
        self.initUI()
        self.buttonConnect()
        self.initSize()
        self.initStyle()
        self.tempVar = 1
        self.browserShow = True
        self.setObjectName('baseWindow')

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        self.setLayout(self.mainLayout)

        self.templateInput = QTextEdit(self)
        self.templateInput.setPlaceholderText('Input message template here')

        self.sendByDateButton = QRadioButton('SendByDate')
        self.sendByIDButton = QRadioButton('SendByID')
        self.searchButton = QRadioButton('Search')
        self.selectButtonBox = QButtonGroup(self)
        self.selectButtonBox.addButton(self.sendByDateButton, 1)
        self.selectButtonBox.addButton(self.sendByIDButton, 2)
        self.selectButtonBox.addButton(self.searchButton, 3)

        self.IDInput = QTextEdit(self)
        self.IDInput.setPlaceholderText('Input ID list here')

        self.startButton = QPushButton('Start')
        self.showLogButton = QPushButton('ShowLog')
        self.showBrowser = QPushButton('Browser')
        self.mainLayout.addSpacing(20)
        self.mainLayout.addWidget(self.templateInput)
        self.mainLayout.addSpacing(20)
        self.tempHBox = QHBoxLayout()
        self.tempHBox.setSpacing(0)
        self.tempHBox.addSpacing(30)
        self.tempHBox.addWidget(self.sendByDateButton)
        self.tempHBox.addWidget(self.sendByIDButton)
        self.tempHBox.addWidget(self.searchButton)

        self.mainLayout.addLayout(self.tempHBox)
        self.mainLayout.addSpacing(20)
        self.mainLayout.addWidget(self.IDInput)
        self.mainLayout.addSpacing(20)
        self.tempH2Box = QHBoxLayout()
        self.tempH2Box.addWidget(self.startButton)
        self.tempH2Box.addWidget(self.showLogButton)
        # self.tempH2Box.addWidget(self.showBrowser)
        # self.mainLayout.addWidget(self.startButton)
        self.mainLayout.addLayout(self.tempH2Box)
        self.mainLayout.addSpacing(20)

        self.sendByDateButton.click()

    def initSize(self):
        # self.templateInput.setFixedSize(460,236)
        # self.IDInput.setFixedSize(460,236)
        self.setFixedWidth(480)
        self.startButton.setMaximumWidth(250)

    def initStyle(self):
        self.setStyleSheet('''QTextEdit{margin-left:20px;
                                    background-color:#f9f9fa;
                                    min-width:440px;
                                    max-width:440px;
                                    min-height:236px;
                                    border-radius:8px;
                                    }
                                QPushButton {
                                background-color: #0081ff;
                                color: white;
                                border-radius: 8px 8px 8px 8px;
                                max-width: 440px;
                                max-height: 44px;
                                width: 440px;
                                height: 44px;
                                margin-left: 20px;
                                margin-right: 20px;
                            }
                            QPushButton:hover {
                                background-color: #0081ff;
                                color: white;
                                border-radius: 8px 8px 8px 8px;
                                max-width: 440px;
                                max-height: 44px;
                                width: 440px;
                                height: 44px;
                                margin-left: 20px;
                                margin-right: 20px;
                                font-weight: bold;
                            }
                            QPushButton:pressed {
                                background-color: #0081ff;
                                color: red;
                                border-radius: 8px 8px 8px 8px;
                                max-width: 440px;
                                max-height: 44px;
                                width: 440px;
                                height: 44px;
                                margin-left: 20px;
                                margin-right: 20px;
                                font-weight: bold;
                            }
                            *#baseWindow{background-color:white;
                                        border:2px solid #0081ff;
                                        border-radius:5px;}''')

    def buttonConnect(self):
        self.showLogButton.clicked.connect(self.hideRightPage)
        self.startButton.clicked.connect(self.startClicked)

    def hideRightPage(self):
        if self.tempVar == 1:
            self.parentWidget().rightFrame.hide()
            # self.parentWidget().setGeometry(500,500)
            self.parentWidget().setFixedWidth(480)
            self.tempVar = 2
        else:
            self.parentWidget().rightFrame.show()
            self.parentWidget().setFixedWidth(1000)
            self.tempVar = 1
    # def hideBrowser(self):
    #     if self.browserShow == True:
    #         self.browserShow = False
    #         assert isinstance(self.parent.driver,webdriver.Chrome)
    #         self.parent.driver
    #     else:
    #         self.browserShow = True

    def startClicked(self):
        if self.selectButtonBox.checkedId() == 1:
            self.workThread = sendByDateClickedThread(self.parent)
            # self.workThread = testThread(self.parent)
        if self.selectButtonBox.checkedId() == 2:
            self.workThread = sendByIDClickedThread(self.parent)
        if self.selectButtonBox.checkedId() == 3:
            self.workThread = searchClickedThread(self.parent)
        self.workThread.start()
        self.parentWidget().s.graySignal.emit()

class RightPage(QScrollArea):
    def __init__(self, parent):
        super(RightPage, self).__init__(parent)
        self.setParent(parent)
        self.initUI()
        self.initStyle()
        self.setObjectName('baseWindow')

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedWidth(520)
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        self.setLayout(self.mainLayout)

        self.titleHBox = QHBoxLayout()
        self.titleHBox.setContentsMargins(0, 0, 0, 0)
        self.titleHBox.setSpacing(0)
        self.titleLabel = QLabel('Process Information')
        self.titleLabel.setObjectName('label1')
        self.scheduleLabel = QLabel('1/100')
        self.scheduleLabel.setObjectName('label2')
        self.titleHBox.addSpacing(30)
        self.titleHBox.addWidget(self.titleLabel)
        # self.titleHBox.addSpacing()
        self.titleHBox.addStretch()
        self.titleHBox.addWidget(self.scheduleLabel)
        self.mainLayout.addSpacing(20)
        self.mainLayout.addLayout(self.titleHBox)
        self.mainLayout.addSpacing(50)
        self.logEdit = QTextEdit()
        self.logEdit.setReadOnly(True)
        self.mainLayout.addWidget(self.logEdit)
        self.mainLayout.addStretch()
        # self.t2 = QTextEdit()
        # self.mainLayout.addWidget(self.t2)

    def initStyle(self):
        self.setStyleSheet('''

        QLabel#label1
        {

            font-family:PingFangSC-Regular;
            font-size:25px;
            color:#080a0d;
            text-align:left;


        }
        QLabel#label2
        {

            color:#0081ff;
            font-size:25px;
            text-align:left;
            margin-right:20px

        }
        QLabel
        {
            
        }
        *#baseWindow{
            background-color:white;
            border:2px solid #0081ff;
            border-radius:5px;
        }
        QTextEdit{
            border:0;
            margin-left:20px;
            color:blue;
        }
        ''')

try:
    app = QApplication(sys.argv)
    t = MyMainWindow()
    t.show()
    app.exec_()
except Exception as e:
    traceback.print_exc()