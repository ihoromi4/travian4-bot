import sys
import configparser

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QAction, qApp
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QIcon

from travlib import login
from travlib import account

config = configparser.ConfigParser()
config.read('config.ini')

lang_dir = 'data/language/'
url = 'http://ts5.travian.ru/'
name = 'broo'
password = '1994igor'

user_agent = config['HEADERS']['user_agent']
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
        self.init_menubar()
        self.init_gui()
        self.show()

    def init_travian(self):
        self.login = login.Login(lang_dir, url, name, password, headers)
        self.account = account.Account(self.login)

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
        label1 = QLabel('fgr', self)
        label2 = QLabel('hjr', self)
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(label1)
        hbox.addWidget(label2)

        self.setLayout(hbox)

win = MainWindow()

sys.exit(app.exec())
