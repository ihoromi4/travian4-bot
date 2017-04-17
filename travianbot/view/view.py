import sys

from PyQt5.QtWidgets import QApplication
import observer

from .mainwindow import MainWindow
from .signindialog import SignUpDialog


class View(observer.Observable):
    def __init__(self, settings: dict):
        super(observer.Observable, self).__init__()

        self.settings = settings

        self.app = QApplication(sys.argv)

        self.mainwindow = MainWindow(settings)

        self.mainwindow.button_add_new_profile.clicked.connect(self.on_click)

    def on_click(self):
        self.on_click()

    def show(self):
        self.mainwindow.show()

        dialog = SignUpDialog(self.mainwindow, self.settings)
        result = dialog.open_dialog()

        print('email:', result['email'])
        print('password:', result['password'])

        sys.exit(self.app.exec())
