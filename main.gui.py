import sys
import configparser

from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon

from travlib import login
from travlib import account

config = configparser.ConfigParser()
config.read('config.ini')

server_url = config['URL']['server_url']
login_url = config['URL']['login_url'].replace('{server_url}', server_url)

name = config['USER']['name']
password = config['USER']['password']

user_agent = config['HEADERS']['user_agent']
headers = {'User-Agent': user_agent}

app = QApplication(sys.argv)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(130, 22, 500, 500)
        self.setWindowTitle('Auto-Travian')
        self.setWindowIcon(QIcon('data/travbot.png'))
        self.init_travian()
        self.init()
        self.show()

    def init_travian(self):
        self.login = login.Login(server_url, name, password, headers)
        self.account = account.Account(self.login)

    def init(self):
        village1 = list(self.account.villages.values())[0]
        self.label = QLabel("village name: {}".format(village1.name), self)

win = MainWindow()

sys.exit(app.exec())
