from PyQt5.QtWidgets import QFrame
from PyQt5 import uic
import observer


class AccountCard(QFrame):
    def __init__(self, parrent, ui: str, account_config: dict):
        QFrame.__init__(self, parrent)

        uic.loadUi(ui, self)

        self.label_server.setText(account_config['server'])
        self.label_username.setText(account_config['username'])

        self.on_account_bot_start = observer.Event()

        self.button_bot_start.clicked.connect(self.on_bot_start)

    def on_bot_start(self):
        self.on_account_bot_start.trigger()
