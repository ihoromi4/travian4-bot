import sys

from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
import observer


class SignUpDialog(QDialog):
    def __init__(self, parrent, settings: dict, profiles_config: dict):
        super(QDialog, self).__init__(parrent)

        uic.loadUi(settings['ui_signindialog'], self)

        self.profiles_config = profiles_config
        self.any_password = '******'

        self.setModal(True)

        self.on_open_profile = observer.Event()

        self.button_exit.clicked.connect(self.exit)
        self.button_ok.clicked.connect(self.ok)

    def get_email(self):
        return self.combobox_emails.currentText()
    email = property(get_email)

    def get_password(self):
        try:
            config = next((i for i in self.profiles_config if i['email'] == self.email))
            if self.edit_password.text() == self.any_password:
                return config['password_sha1']
            else:
                return self.edit_password.text()
        except StopIteration:
            return self.edit_password.text()
    password = property(get_password)

    def get_config(self):
        try:
            return next((i for i in self.profiles_config if i['email'] == self.email))
        except StopIteration:
            return {}
    config = property(get_config)

    def validate_password(self, password: str):
        return True

    def open_dialog(self):
        password = '******'

        for profile in self.profiles_config:
            self.combobox_emails.addItem(profile['email'])

        self.edit_password.setText(password)

        self.show()
        self.exec()

        self.on_open_profile.trigger(self.config)

        return {
            'email': self.email,
            'password': self.password
        }

    def exit(self):
        sys.exit()

    def ok(self):
        if self.validate_password(self.password):
            super(QDialog, self).close()
