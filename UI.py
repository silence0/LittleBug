from PyQt5 import QtWidgets
import time
from PyQt5.QtCore import QDate
from PyQt5.QtCore import QThread
from PyQt5.QtCore import QTime
import datetime
import sys
import AllDatas
import TheLastDayDatas


class MyQThreadTheseDays(QThread):
    def __init__(self, startDate, endDate, window):
        super(MyQThreadTheseDays, self).__init__()
        assert isinstance(startDate, datetime.date)
        assert isinstance(endDate, datetime.date)
        self.startDate = startDate
        self.endDate = endDate
        self.window = window

    def run(self):
        TheLastDayDatas.getDatas(self.startDate.year, self.startDate.month, self.startDate.day,
                                 self.endDate.year, self.endDate.month, self.endDate.day)
        # self.thisDayButton.setEnabled(True)
        self.window.thisDayButton.setEnabled(True)
        self.window.allDayButton.setEnabled(True)
        # self.window.show()


class MyQThreadAllDays(QThread):
    def __init__(self, window):
        super(MyQThreadAllDays, self).__init__()
        self.window = window

    def run(self):
        AllDatas.allDateExcelGetTopInterface()
        self.window.thisDayButton.setEnabled(True)
        self.window.allDayButton.setEnabled(True)
        # self.window.show()
class MyQThreadTimer(QThread):
    def __init__(self,window):
        super(MyQThreadTimer, self).__init__()
        self.window = window
    def run(self):
        if self.judgeTimeMeet() == True:
            yesterday = datetime.datetime.now()+datetime.timedelta(-1)
            TheLastDayDatas.getDatas(yesterday.year,yesterday.month,yesterday.day,
                                     yesterday.year,yesterday.month,yesterday.day)
    def setTime(self,hour,minute):
        self.hour = hour
        self.minute = minute
    def judgeTimeMeet(self):
        while True:
            now = datetime.datetime.now()
            if self.hour == now.hour and self.minute == now.minute:
                return True
class myWindows(QtWidgets.QScrollArea):
    def __init__(self):
        super(myWindows, self).__init__()
        self.allDayButton = QtWidgets.QPushButton('allDays', self)
        self.thisDayButton = QtWidgets.QPushButton('selectedDays', self)
        self.calendarStart = QtWidgets.QCalendarWidget()
        self.calendarEnd = QtWidgets.QCalendarWidget()
        self.timer = QtWidgets.QTimeEdit()
        # self.timer.setTime(datetime.datetime.now())
        self.subscribeButton = QtWidgets.QPushButton('subscribe',self)
        self.resize(200, 300)
        self.myLayout = QtWidgets.QHBoxLayout()
        self.myLayout.addWidget(self.calendarStart)
        self.myLayout.addWidget(self.calendarEnd)
        self.myLayout.addWidget(self.thisDayButton)
        self.myLayout.addWidget(self.allDayButton)
        self.myLayout.addWidget(self.timer)
        self.myLayout.addWidget(self.subscribeButton)
        self.setLayout(self.myLayout)
        self.thisDayButton.clicked.connect(self.thisDayClicked)
        self.allDayButton.clicked.connect(self.allDayClicked)
        self.subscribeButton.clicked.connect(self.subscribeClicked)

    def thisDayClicked(self):
        # print(self.calendar.monthShown())
        # print(self.calendar.yearShown())
        # print(self.calendar.show)
        # print(self.calendar.selectedDate())
        dateStart = self.calendarStart.selectedDate()
        dateEnd = self.calendarEnd.selectedDate()
        assert isinstance(dateStart, QDate)
        assert isinstance(dateEnd, QDate)
        pyDateStart = datetime.date(dateStart.year(), dateStart.month(), dateStart.day())
        pyDateEnd = datetime.date(dateEnd.year(), dateEnd.month(), dateEnd.day())
        # print(pyDate)
        self.thisDayButton.setEnabled(False)
        self.allDayButton.setEnabled(False)
        # self.hide()
        self.th = MyQThreadTheseDays(pyDateStart, pyDateEnd, self)
        self.th.start()

    def allDayClicked(self):
        self.allDayButton.setEnabled(False)
        self.thisDayButton.setEnabled(False)
        # AllDatas.allDateExcelGetTopInterface()
        # self.hide()
        self.th2 = MyQThreadAllDays(self)
        self.th2.start()

    def subscribeClicked(self):
        self.th3 = MyQThreadTimer(self)
        selectTime = self.timer.time()
        assert isinstance(selectTime,QTime)
        self.th3.setTime(selectTime.hour(),selectTime.minute())
        self.th3.start()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    t = myWindows()
    t.show()
    sys.exit(app.exec_())
