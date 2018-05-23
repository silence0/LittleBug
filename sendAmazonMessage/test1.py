from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
class MyWindow(QWidget):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.initUI()
    def initUI(self):
        self.mainLayout = QHBoxLayout()
        self.l1 = QLabel('12')
        self.l2 = QLabel('123')
        self.l3 = QLabel('123')
        self.l4 = QLabel('456')
        self.l5 = QLabel('456')
        self.mainLayout.addWidget(self.l1)
        self.mainLayout.addWidget(self.l2)
        self.mainLayout.addWidget(self.l3)
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.l1.setMaximumWidth(self.l1.fontMetrics().width(self.l1.text()))
        # self.l1.setWordWrap(True)
        self.mainLayout.setSpacing(0)
        self.setLayout(self.mainLayout)
        self.mainLayout.setSizeConstraint(self.mainLayout.SetFixedSize)
        # self.childLayout = QHBoxLayout()
        # self.childLayout.addWidget(self.l4)
        # self.childLayout.addWidget(self.l5)
        # self.childLayout.setSpacing(0)
        # self.childLayout.setContentsMargins(0,0,0,0)
        # self.mainLayout.addLayout(self.childLayout)
if __name__=='__main__':
    app = QApplication(sys.argv)
    t = MyWindow()
    t.show()
    app.exec_()