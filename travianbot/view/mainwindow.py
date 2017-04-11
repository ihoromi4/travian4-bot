import PyQt5.QtWidgets as qtwidgets
from PyQt5.QtWidgets import QApplication, qApp
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QAction, QPushButton
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5 import uic


class MainWindow(QMainWindow):
    def __init__(self, settings: dict):
        super().__init__()

        self.settings = settings
        # ---
        uic.loadUi(settings['ui_mainwindow'], self)

        self.setGeometry(130, 22, 500, 500)
        self.setWindowTitle('Auto-Travian')

        icon = QIcon(settings['icon_path'])
        self.setWindowIcon(icon)

        self.statusbar = self.statusBar()
        self.status = "Ready to work!"
        # self.init_menubar()

    def get_status(self) -> str:
        return ''

    def set_status(self, message: str) -> None:
        self.statusbar.showMessage(message)
    status = property(get_status, set_status)

    def init_menubar(self):
        icon = QIcon(self.settings['icon_path'])

        exit_action = QAction(icon, '&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(qApp.exit)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(exit_action)
