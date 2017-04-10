import sys

from PyQt5.QtWidgets import QApplication

from .mainwindow import MainWindow


class View:
    def __init__(self, settings: dict):
        self.settings = settings

        self.app = QApplication(sys.argv)

        self.win = MainWindow(settings)

    def show(self):
        self.win.show()
        sys.exit(self.app.exec())
