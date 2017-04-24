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

    def open_dialog(self, profiles_config: dict):
        config = profiles_config[0]

        password = '******'

        self.edit_email.setText(config['email'])
        self.edit_password.setText(password)

        self.show()
        self.exec()

        if self.edit_password.text() != password:
            password = self.edit_password.text()
        else:
            password = config['password_sha1']

        return {
            'email': self.edit_email.text(),
            'password': password
        }

    def exit(self):
        sys.exit()

    def close(self):
        super(QDialog, self).close()
