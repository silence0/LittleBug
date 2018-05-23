from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
class MyWindow(QFrame):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)

    def mousePressEvent(self, event:QMouseEvent):
        if event.button()==Qt.LeftButton:
            self.drag = True
            event.accept()
        if event.button()==Qt.RightButton:
            print(456)
    def mouseMoveEvent(self, event:QMouseEvent):
        if self.drag == True:
            self.move(event.globalPos()-event.)


app = QApplication(sys.argv)
t = MyWindow()
t.show()
app.exec_()