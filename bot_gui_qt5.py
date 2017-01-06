import sys
import configparser

import PyQt5.QtWidgets as qtwidgets
from PyQt5.QtWidgets import QApplication, qApp
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QAction, QPushButton
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QIcon

from travlib import login
from travlib import account

url = 'http://ts5.travian.ru/'
name = 'broo'
password = 'wA4iN_tYR'

user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'
headers = {'User-Agent': user_agent}

app = QApplication(sys.argv)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(130, 22, 500, 500)
        self.setWindowTitle('Auto-Travian')
        self.setWindowIcon(QIcon('data/travbot.png'))
        # self.init_travian()
        # self.init()
        self.statusbar = self.statusBar()
        self.statusbar.showMessage("Ready to work!")
        # ---
        self.init_menubar()
        self.init_gui()
        self.show()

    def init_travian(self):
        self.account = account.Account(url, name, password, headers)

    def init(self):
        for village in self.account.villages:
            self.label = QLabel("village name: {}".format(village.name), self)

    def init_menubar(self):
        exit_action = QAction(QIcon('data/travbot.png'), '&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(qApp.exit)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(exit_action)

    def init_gui(self):
        widget = QWidget(self)
        policy = qtwidgets.QSizePolicy(
            qtwidgets.QSizePolicy.Preferred,
            qtwidgets.QSizePolicy.Preferred)
        widget.setSizePolicy(policy)
        #widget.setFixedSize(300, 300)

        label1 = QLabel('fgr')
        label2 = QLabel('hjr')
        btn = QPushButton('Button')
        btn.move(50, 50)
        box = QVBoxLayout()
        box.addStretch(1)
        box.addWidget(label1)
        box.addWidget(label2)
        box.addWidget(btn)

        widget.setLayout(box)

win = MainWindow()

sys.exit(app.exec())
