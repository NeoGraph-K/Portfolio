import sys
from datetime import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from calendar import *
import pymongo

class TodoManage(QWidget):
    
    def CreateCalendar(self, year, month):
        begin, maxdays = monthrange(self.year, self.month)
        begins = True
        days = []
        daycount = 1
        for week in range(6):
            days.append([])
            for day in range(7):
                if begins:
                    if begin == day:
                        begins = False
                        days[week].append(daycount)
                        daycount+=1
                else:
                    if daycount <= maxdays:
                        days[week].append(daycount)
                        daycount+=1
        for week in range(5):
            if len(days[week]) != 0:
                if week == 0:
                    days[week + 1].insert(0, days[week].pop())
                elif len(days[week]) > 7:
                    days[week + 1].insert(0, days[week].pop())
        if len(days[0]) == 0:
            del days[0]
        if len(days[-1]) == 0:
            del days[-1]
        if len(days[-1]) == 0:
            del days[-1]
        if len(days[-1]) == 0:
            del days[-1]
        self.days = days
    
    def DaysButtonRefresh(self, year, month):
        self.CreateCalendar(year,month)
        for row in self.daysbutton:
            for cell in row:
                cell.setText("")
        drow, dcell = 0, 0
        for row in range(len(self.days)):
            for cell in range(7):
                if row == 0:
                    if 7 - len(self.days[row]) <= cell:
                        self.daysbutton[row][cell].setText(str(self.days[drow][dcell]))
                        dcell+=1
                else:
                    if len(self.days[row]) > cell:
                        self.daysbutton[row][cell].setText(str(self.days[drow][dcell]))
                        dcell+=1
            drow += 1
            dcell = 0
        self.monthtitle.setText("%4s년 %4s월" % (self.year, self.month))
    
    def NextMonth(self):
        self.month += 1
        if self.month > 12:
            self.year += 1
            self.month = 1
        self.DaysButtonRefresh(self.year, self.month)
        self.CallDay(1)
    
    def PrevMonth(self):
        self.month -= 1
        if self.month < 1:
            self.year -= 1
            self.month = 12
        self.DaysButtonRefresh(self.year, self.month)
        self.CallDay(1)
    
    def CallDay(self, day):
        self.day = day
        self.DeleteLayout(self.todoview.layout)
        todos = self.db.Todos
        finds = todos.find({"userid":self.userid,
                            "year":self.year,
                            "month":self.month,
                            "day":self.day})
        for find in finds:
            self.InsertTodo(find["check"], find["title"])
        
    def TodoCheck(self, value):
        checked = self.sender()
        if checked.isChecked():
            checked.line["Label"].setStyleSheet("text-decoration:line-through")
        else:
            checked.line["Label"].setStyleSheet("")
        todos = self.db.Todos
        todos.update({"userid":self.userid,
                      "title":checked.line["Label"].text()},
                     {"$set":{"check":checked.isChecked()}})
        
    def InsertTodo(self, checked, label):
        temp = {}
        self.todoview.todos.append(temp)
        self.todoview.todos[-1]["Check"] = QCheckBox()
        self.todoview.todos[-1]["Check"].setFont(QFont(self.font["name"], self.font["size"]))
        self.todoview.todos[-1]["Check"].setChecked(checked)
        self.todoview.todos[-1]["Check"].stateChanged.connect(self.TodoCheck)
        self.todoview.todos[-1]["Check"].line = temp
        self.todoview.layout.addWidget(self.todoview.todos[-1]["Check"], len(self.todoview.todos) + 0, 0, 1, 1)
        
        self.todoview.todos[-1]["Label"] = QLabel("")
        self.todoview.todos[-1]["Label"].setText(label)
        self.todoview.todos[-1]["Label"].setAlignment(Qt.AlignLeft)
        self.todoview.todos[-1]["Label"].setFont(QFont(self.font["name"], self.font["size"]))
        if checked:
            self.todoview.todos[-1]["Label"].setStyleSheet("text-decoration:line-through")
        self.todoview.layout.addWidget(self.todoview.todos[-1]["Label"], len(self.todoview.todos) + 0, 1, 1, 4)
        
        self.todoview.todos[-1]["Del"] = QPushButton("")
        self.todoview.todos[-1]["Del"].setText("삭제")
        self.todoview.todos[-1]["Del"].setFont(QFont(self.font["name"], self.font["size"]))
        self.todoview.todos[-1]["Del"].line = self.todoview.todos[-1]
        self.todoview.todos[-1]["Del"].clicked.connect(self.DeleteTodo)
        self.todoview.todos[-1]["Del"].layout = self.todoview.layout
        self.todoview.layout.addWidget(self.todoview.todos[-1]["Del"], len(self.todoview.todos) + 0, 5, 1, 1)
    
    def DeleteTodo(self):
        button = self.sender()
        todos = self.db.Todos
        todos.delete_one({"userid":self.userid,
                          "title":button.line["Label"].text()})
        button.layout.removeWidget(button.line["Check"])
        button.line["Check"].setParent(None)
        button.layout.removeWidget(button.line["Del"])
        button.line["Del"].setParent(None)
        button.layout.removeWidget(button.line["Label"])
        button.line["Label"].setParent(None)
        
    def DeleteLayout(self, layout):
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()
                elif child.layout() is not None:
                    self.DeleteLayout(child.layout())
            
    def PushTodo(self):
        self.InsertTodo(False, self.titleedit.text())    
        todos = self.db.Todos
        todo = {
            "userid":self.userid,
            "title":self.titleedit.text(),
            "year":self.year,
            "month":self.month,
            "day":self.day,
            "check":False
        }
        todos.insert(todo)
        self.titleedit.setText("")
        
    def DaysButton(self):
        text = self.sender().text()
        if len(text) > 0:
            self.CallDay(int(text))
        
    def __init__(self, db, userid):
        super().__init__()
        self.db = db
        self.userid = userid
        self.tabname = "일정"
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.font = {"name":"Arial", "size": 15}
        
        self.prevbutton = QPushButton("이전달")
        self.prevbutton.setMaximumHeight(60)
        self.prevbutton.setFont(QFont(self.font["name"], self.font["size"]))
        self.prevbutton.clicked.connect(self.PrevMonth)
        self.layout.addWidget(self.prevbutton, 0, 0, 1, 1)
        
        self.monthtitle = QLabel("월")
        self.layout.addWidget(self.monthtitle,0, 1, 1, 5)
        self.monthtitle.setFont(QFont(self.font["name"], self.font["size"]))
        
        self.nextbutton = QPushButton("다음달")
        self.nextbutton.setMaximumHeight(60)
        self.nextbutton.setFont(QFont(self.font["name"], self.font["size"]))
        self.nextbutton.clicked.connect(self.NextMonth)
        self.layout.addWidget(self.nextbutton, 0, 6, 1, 1)
        
        self.weeks = []
        temp = ["일","월","화","수","목","금","토"]
        cnt = 0
        for lab in temp:
            self.weeks.append(QLabel(lab))
            self.weeks[-1].setAlignment(Qt.AlignCenter)
            self.weeks[-1].setFont(QFont(self.font["name"], self.font["size"]))
            self.layout.addWidget(self.weeks[-1], 1, 0 + cnt, 1, 1)
            cnt+=1
        self.daysbutton = []
        for row in range(6):
            self.daysbutton.append([])
            for cell in range(7):
                self.daysbutton[row].append(QPushButton(""))
                self.daysbutton[row][cell].setMaximumHeight(60)
                self.daysbutton[row][cell].setFont(QFont(self.font["name"], self.font["size"]))
                self.daysbutton[row][cell].clicked.connect(self.DaysButton)
                self.daysbutton[row][cell].setStyleSheet(" background-color:aqua; ")
                self.layout.addWidget(self.daysbutton[row][cell],2+row, 0+cell, 1, 1)
        
        self.todoview = QScrollArea()
        self.todoview.todos = []
        self.todoview.layout = QGridLayout()
        self.todoview.setLayout(self.todoview.layout)
        self.layout.addWidget(self.todoview, 0, 8, 6, 4)
        temp = QLabel("이름")
        temp.setAlignment(Qt.AlignCenter)
        temp.setFont(QFont(self.font["name"], self.font["size"]))
        self.layout.addWidget(temp, 6, 8, 1, 1)
        
        self.titleedit = QLineEdit()
        self.layout.addWidget(self.titleedit, 6, 9, 1, 3)
        self.titleedit.setMaximumHeight(60)
        self.titleedit.setFont(QFont(self.font["name"], self.font["size"]))
        
        self.insertbutton = QPushButton("등록")
        self.layout.addWidget(self.insertbutton, 7, 10, 1, 2)
        self.insertbutton.setMaximumHeight(60)
        self.insertbutton.setFont(QFont(self.font["name"], self.font["size"]))
        self.insertbutton.setStyleSheet(" background-color:aqua; ")
        self.insertbutton.clicked.connect(self.PushTodo)
        self.titleedit.returnPressed.connect(self.insertbutton.click)
        
        self.monthtitle.setAlignment(Qt.AlignCenter)
        
        self.today = datetime.today()
        self.year, self.month = self.today.year, self.today.month
        self.DaysButtonRefresh(self.today.year, self.today.month)
        
        self.CallDay(self.today.day)