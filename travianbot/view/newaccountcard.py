from PyQt5.QtWidgets import QFrame
from PyQt5 import uic
import observer


class NewAccountCard(QFrame):
    def __init__(self, parrent, ui: str):
        QFrame.__init__(self, parrent)

        uic.loadUi(ui, self)

        self.on_save = observer.Event()

        self.button_save.clicked.connect(self._on_save)

    def _on_save(self):
        self.on_save.trigger()

    def get_account_config(self):
        return {
            'server': self.combobox_server.currentText(),
            'username': self.edit_username.text(),
            'password': self.edit_password.text()
        }
