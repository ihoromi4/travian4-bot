import sys

from PyQt5.QtWidgets import QDialog
from PyQt5 import uic


class SignUpDialog(QDialog):
    def __init__(self, parrent, settings: dict):
        super(QDialog, self).__init__(parrent)

        uic.loadUi(settings['ui_signindialog'], self)

        self.setModal(True)

        self.button_exit.clicked.connect(self.exit)
        self.button_ok.clicked.connect(self.close)

    def open_dialog(self, config: dict):
        self.edit_email.setText(config['email'])
        self.edit_password.setText(config['password'])

        self.show()
        self.exec()

        return {
            'email': self.edit_email.text(),
            'password': self.edit_password.text()
        }

    def exit(self):
        sys.exit()

    def close(self):
        super(QDialog, self).close()
