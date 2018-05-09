from PyQt5 import QtWidgets
import time
from PyQt5.QtCore import QDate
from PyQt5.QtCore import QThread
import datetime
import sys
import AllDatas
import TheLastDayDatas
class MyQThreadTheseDays(QThread):
    def __init__(self,startDate,endDate):
        super(MyQThreadTheseDays, self).__init__()
        assert isinstance(startDate,datetime.date)
        assert isinstance(endDate,datetime.date)
        self.startDate = startDate
        self.endDate = endDate
    def run(self):
        TheLastDayDatas.getDatas(self.startDate.year,self.startDate.month,self.startDate.day,
                                 self.endDate.year,self.endDate.month,self.endDate.day)

class MyQThreadAllDays(QThread):
    def __init__(self):
        super(MyQThreadAllDays, self).__init__()
    def run(self):
        AllDatas.allDateExcelGetTopInterface()
class myWindows(QtWidgets.QScrollArea):
    def __init__(self):
        super(myWindows, self).__init__()
        self.allDayButton =QtWidgets.QPushButton('allDays',self)
        self.thisDayButton = QtWidgets.QPushButton('selectedDays',self)
        self.calendarStart = QtWidgets.QCalendarWidget()
        self.calendarEnd = QtWidgets.QCalendarWidget()
        self.resize(200,300)
        self.myLayout = QtWidgets.QHBoxLayout()
        self.myLayout.addWidget(self.calendarStart)
        self.myLayout.addWidget(self.calendarEnd)
        self.myLayout.addWidget(self.thisDayButton)
        self.myLayout.addWidget(self.allDayButton)
        self.setLayout(self.myLayout)
        self.thisDayButton.clicked.connect(self.thisDayClicked)
        self.allDayButton.clicked.connect(self.allDayClicked)
    def thisDayClicked(self):
        # print(self.calendar.monthShown())
        # print(self.calendar.yearShown())
        # print(self.calendar.show)
        # print(self.calendar.selectedDate())
        dateStart = self.calendarStart.selectedDate()
        dateEnd = self.calendarEnd.selectedDate()
        assert isinstance(dateStart,QDate)
        assert isinstance(dateEnd,QDate)
        pyDateStart = datetime.date(dateStart.year(),dateStart.month(),dateStart.day())
        pyDateEnd = datetime.date(dateEnd.year(),dateEnd.month(),dateEnd.day())
        # print(pyDate)
        self.thisDayButton.setEnabled(False)
        self.th = MyQThreadTheseDays(pyDateStart,pyDateEnd)
        self.th.start()
        self.thisDayButton.setEnabled(True)
    def allDayClicked(self):
        self.allDayButton.setEnabled(False)
        # AllDatas.allDateExcelGetTopInterface()
        self.th2 = MyQThreadAllDays()
        self.th2.start()
        self.allDayButton.setEnabled(True)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    t = myWindows()
    t.show()
    sys.exit(app.exec_())

