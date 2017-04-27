import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5 import uic
import observer

from .mainwindow import MainWindow
from .signindialog import SignUpDialog


class View(observer.Observable):
    def __init__(self, ui_config: dict, profiles_config: dict):
        super(observer.Observable, self).__init__()

        self.ui_config = ui_config
        self.profiles_config = profiles_config

        # events
        self.on_new_account = observer.Event()
        self.on_open_profile = observer.Event()

        self.init_gui()

        # connected actions
        action = lambda: self.on_new_account.trigger()
        self.mainwindow.button_new_account.clicked.connect(action)

    def init_gui(self):
        self.app = QApplication(sys.argv)
        self.mainwindow = MainWindow(self.ui_config)

    def show(self):
        self.mainwindow.show()

        dialog = SignUpDialog(self.mainwindow, self.ui_config, self.profiles_config)
        dialog.on_open_profile.on(lambda config: self.on_open_profile.trigger(config))
        result = dialog.open_dialog()

        print('email:', result['email'])
        print('password:', result['password'])

        sys.exit(self.app.exec())

    def new_account_card(self):
        widget_cards_id = 0
        parrent = self.mainwindow.stacked_widget.widget(widget_cards_id)

        frame = QFrame(parrent)
        uic.loadUi(self.ui_config['ui_newplayingcard'], frame)

        layout = parrent.findChild(QHBoxLayout)
        items_count = layout.count()
        offset = 2
        layout.insertWidget(items_count - offset, frame)

        frame.show()

    def add_account_card(self, account_config: dict):
        widget_cards_id = 0
        parrent = self.mainwindow.stacked_widget.widget(widget_cards_id)

        frame = QFrame(parrent)
        uic.loadUi(self.ui_config['ui_playingcard'], frame)

        layout = parrent.findChild(QHBoxLayout)
        items_count = layout.count()
        offset = 2
        layout.insertWidget(items_count - offset, frame)

        frame.label_server.setText(account_config['server'])
        frame.label_username.setText(account_config['username'])

        frame.show()
