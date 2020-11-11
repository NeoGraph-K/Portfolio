import sys
from datetime import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont

class MoneyManage(QWidget):
    def __init__(self, db, userid):
        super().__init__()
        self.db = db
        self.userid = userid
        self.tabname = "재정"
        self.layout = QGridLayout()
        self.setLayout(self.layout)