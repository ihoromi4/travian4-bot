import configparser
import time
import random

import requests
import notify2

from travlib import login
from travlib import account


notify2.init('travian daemon')


class Watcher:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')

        lang_dir = 'data/language/'
        url = 'http://ts5.travian.ru/'
        name = 'broo'
        password = '1994igor'

        user_agent = config['HEADERS']['user_agent']
        headers = {'User-Agent': user_agent}

        self.login = login.Login(lang_dir, url, name, password, headers)
        print('Travian version:', self.login.game_version)

        self.account = account.Account(self.login)

watcher = Watcher()
watcher.watch()
