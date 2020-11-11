import sys
from datetime import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont
import pymongo
import moneymanage
import todomanage

class Application(QWidget):
    def __init__(self):
        super().__init__()
        self.Initialize("Management", "icon.png", 1000, 600)
        
    def Connect(self):
        self.client = pymongo.MongoClient("mongodb+srv://clusterpassword:134Xweqr87F5Xqr1SOZGOZP7qz1@bgcluster.q9aok.mongodb.net/Persnal_DB?retryWrites=true&w=majority")
        self.client = self.client.Persnal_DB
        
    def Initialize(self, title, icon, width, height):
        self.Connect()
        self.userid = QInputDialog.getText(self, "아이디", "아이디를 입력하세요")[0].upper()
        password = QInputDialog.getText(self, "비밀번호", "비밀번호를 입력하세요")
        users = self.client.Users
        user = users.find_one({"userid":self.userid})
        if user is None:
            users.insert({"userid":self.userid,
                          "password":password})
        else:
            if user["password"] != password:
                sys.exit()
        self.tablist = []
        self.tablist.append(todomanage.TodoManage(self.client, self.userid))
        self.tablist.append(moneymanage.MoneyManage(self.client, self.userid))
        self.tabs = QTabWidget()
        for tab in self.tablist:
            self.tabs.addTab(tab, tab.tabname)
        self.layout = QGridLayout()
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        self.setWindowIcon(QIcon(icon))
        self.setWindowTitle(title)
        self.resize(width,height)
        self.show()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Application()
    sys.exit(app.exec_())