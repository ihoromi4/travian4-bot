import sys

from PyQt5.QtWidgets import QApplication
import observer

from .mainwindow import MainWindow


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
        sys.exit(self.app.exec())
