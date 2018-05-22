from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.resize(500, 600)
        self.templateInput = QTextEdit()
        self.startButton = QPushButton('start')
        self.selectionGroup = QButtonGroup()
        self.selectionGroup.addButton(QRadioButton('1'))
        self.selectionGroup.addButton(QRadioButton('2'))
        self.selectionGroup.addButton(QRadioButton('3'))

        # self.setFlag(Qt.CustomizeWindowHint)


class Title(QFrame):
    def __init__(self, parent):
        super(Title, self).__init__(parent)
        self.parent = parent
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.initUI()
        # self.resize(1000,1000)
        # self.setMinimumSize(480,32)

    def initUI(self):
        self.titleLabel = QLabel('Spider')
        self.closeLabel = QLabel('×')
        self.miniLabel = QLabel('-')
        # self.miniLabel.setMaximumWidth(self.miniLabel.fontMetrics().width(self.miniLabel.text()))
        # self.titleLabel.setMaximumWidth(self.titleLabel.fontMetrics().width(self.titleLabel.text()))
        # self.closeLabel.setMaximumWidth(self.closeLabel.fontMetrics().width(self.closeLabel.text()))
        # self.miniLabel.setMaximumHeight(10)

        self.myLayout = QHBoxLayout()

        self.myLayout.addSpacing(20)
        self.myLayout.addWidget(self.titleLabel)
        self.myLayout.addSpacing(350)
        self.myLayout.addWidget(self.miniLabel)
        self.myLayout.addSpacing(0)
        self.myLayout.addWidget(self.closeLabel)
        # self.myLayout.addSpacing(20)
        self.myLayout.setSpacing(0)
        self.myLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.myLayout)


        f = open('t1.css')
        self.setStyleSheet(f.read())

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


class T(QFrame):
    def __init__(self):
        super(T, self).__init__(None, Qt.Window)

        self.resize(480, 700)
        # self.resize(1000, 700)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.titleWidget = Title(self)
        self.titleWidget.setObjectName('aaa')
        self.templateText = QTextEdit()
        self.templateText.setPlaceholderText('Please input message template here')
        self.IDText = QTextEdit()
        self.radioBox = QButtonGroup()
        self.sendByID = QRadioButton('SendByID')
        self.sendByDate = QRadioButton('SendByDate')
        self.search = QRadioButton('Search')
        self.radioBox.addButton(self.sendByID)
        self.radioBox.addButton(self.sendByDate)
        self.radioBox.addButton(self.search)
        self.startButton = QPushButton('Start')

        self.myLayout = QVBoxLayout()
        self.myLayout.addWidget(self.titleWidget)
        # self.myLayout.addSpacing(20)
        self.myLayout.addWidget(self.templateText)

        self.tempHBoxLayout = QHBoxLayout()
        self.tempHBoxLayout.addSpacing(20)
        self.tempHBoxLayout.addWidget(self.sendByID)
        self.tempHBoxLayout.addWidget(self.sendByDate)
        self.tempHBoxLayout.addWidget(self.search)
        self.myLayout.addSpacing(20)
        self.myLayout.addLayout(self.tempHBoxLayout)
        self.myLayout.addSpacing(20)
        self.myLayout.addWidget(self.IDText)
        self.IDText.hide()
        self.myLayout.addWidget(self.startButton)
        self.myLayout.addSpacing(20)

        self.setLayout(self.myLayout)
        self.sendByID.clicked.connect(self.showIDText)
        self.sendByDate.clicked.connect(self.hideIDText)
        self.search.clicked.connect(self.hideIDText)
        self.myLayout.setContentsMargins(0, 0, 0, 0)
        self.myLayout.setSpacing(0)
        self.myLayout.addStretch()
        t = open('t.css')
        s = t.read()
        self.setStyleSheet(s)

    def showIDText(self):
        self.IDText.show()

    def hideIDText(self):
        self.IDText.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    t = T()
    t.setObjectName('mainWindow')
    t.show()

    app.exec_()
