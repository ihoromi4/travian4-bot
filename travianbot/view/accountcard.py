from PyQt5.QtWidgets import QFrame
from PyQt5 import uic
import observer


class AccountCard(QFrame):
    def __init__(self, parrent, ui: str, account_config: dict):
        QFrame.__init__(self, parrent)

        uic.loadUi(ui, self)

        self.label_server.setText(account_config['server'])
        self.label_username.setText(account_config['username'])
