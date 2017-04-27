import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5 import uic
import observer

from .mainwindow import MainWindow
from .signindialog import SignUpDialog
from .newaccountcard import NewAccountCard
from .accountcard import AccountCard


class View(observer.Observable):
    def __init__(self, ui_config: dict, profiles_config: dict):
        super(observer.Observable, self).__init__()

        self.ui_config = ui_config
        self.profiles_config = profiles_config
        self._new_card = None

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
        if self._new_card:
            return

        widget_cards_id = 0
        parrent = self.mainwindow.stacked_widget.widget(widget_cards_id)

        ui = self.ui_config['ui_newplayingcard']

        card = self._new_card = NewAccountCard(parrent, ui)
        card.on_save.on(self.save_new_account_card)

        layout = parrent.findChild(QHBoxLayout)
        items_count = layout.count()
        offset = 2
        layout.insertWidget(items_count - offset, card)

        self.mainwindow.button_new_account.hide()
        #card.show()

    def save_new_account_card(self):
        widget_cards_id = 0
        parrent = self.mainwindow.stacked_widget.widget(widget_cards_id)

        layout = parrent.findChild(QHBoxLayout)
        layout.removeWidget(self._new_card)

        account_config = self._new_card.get_account_config()

        self._new_card.hide()
        self._new_card.destroy()
        self._new_card = None

        self.add_account_card(account_config)

        self.mainwindow.button_new_account.show()

    def add_account_card(self, account_config: dict):
        widget_cards_id = 0
        parrent = self.mainwindow.stacked_widget.widget(widget_cards_id)

        ui = self.ui_config['ui_playingcard']

        card = AccountCard(parrent, ui, account_config)

        layout = parrent.findChild(QHBoxLayout)
        items_count = layout.count()
        offset = 2
        layout.insertWidget(items_count - offset, card)
