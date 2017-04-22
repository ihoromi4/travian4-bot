import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5 import uic
import observer

from .mainwindow import MainWindow
from .signindialog import SignUpDialog


class View(observer.Observable):
    def __init__(self, settings: dict, config: dict):
        super(observer.Observable, self).__init__()

        self.settings = settings
        self.config = config

        # events
        self.on_new_account = observer.Event()

        self.init_gui()

        # connected actions
        action = lambda: self.on_new_account.trigger()
        self.mainwindow.button_new_account.clicked.connect(action)

    def init_gui(self):
        self.app = QApplication(sys.argv)
        self.mainwindow = MainWindow(self.settings)

    def show(self):
        self.mainwindow.show()

        dialog = SignUpDialog(self.mainwindow, self.settings)
        result = dialog.open_dialog(self.config)

        print('email:', result['email'])
        print('password:', result['password'])

        sys.exit(self.app.exec())

    def add_account_card(self, config: dict):
        widget_cards_id = 0
        parrent = self.mainwindow.stacked_widget.widget(widget_cards_id)

        frame = QFrame(parrent)
        uic.loadUi(self.settings['ui_playingcard'], frame)

        layout = parrent.findChild(QHBoxLayout)
        items_count = layout.count()
        offset = 2
        layout.insertWidget(items_count - offset, frame)

        frame.label_server.setText(config['server'])
        frame.label_username.setText(config['username'])

        frame.show()
