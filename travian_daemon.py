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

    def watch(self):
        target_village_id = 79385
        target_village = self.account._villages[target_village_id]
        while True:
            for village in self.account.villages:
                if village.id == target_village_id:
                    continue
                if village.id != 75423:
                    continue
                if village.inside.marketplace.free_merchants == 0:
                    continue
                marketplace = village.inside.marketplace
                transfer_percent = 3 / 17.6
                resources = village.resources
                warehouse = village.warehouse
                granary = village.granary
                if resources[account.LUMBER] / warehouse > transfer_percent:
                    if village.inside.marketplace.free_merchants > 0:
                        marketplace.send_resources(target_village.pos, (500, 0, 0, 0))
                        print('send lumber')
                if resources[account.CLAY] / warehouse > transfer_percent:
                    if village.inside.marketplace.free_merchants > 0:
                        marketplace.send_resources(target_village.pos, (0, 500, 0, 0))
                        print('send clay')
                if resources[account.IRON] / warehouse > transfer_percent:
                    if village.inside.marketplace.free_merchants > 0:
                        marketplace.send_resources(target_village.pos, (0, 0, 500, 0))
                        print('send iron')
                #if resources[account.CROP] / granary > transfer_percent:
                #    if village.inside.marketplace.free_merchants > 0:
                #        marketplace.send_resources(target_village.pos, (0, 0, 0, 500))
                #        print('send crop')
            print('while iteration', time.time())
            time.sleep(30 + 30 * random.random())

watcher = Watcher()
watcher.watch()
