import configparser
import time
import random

import notify2

from travlib import login
from travlib import account


notify2.init('travian daemon')


class Watcher:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')

        server_url = config['URL']['server_url']

        name = config['USER']['name']
        password = config['USER']['password']

        user_agent = config['HEADERS']['user_agent']
        headers = {'User-Agent': user_agent}

        self.login = login.Login(server_url, name, password, headers)
        print('Travian version:', self.login.game_version)

        self.account = account.Account(self.login)

    def watch(self):
        while True:
            title = 'Travian notification:'
            msg = ''
            to_show = False
            warning_percent = 0.9
            for village in self.account.villages:
                msg += 'Village: {}\n'.format(village.name)
                resources = village.resources
                warehouse = village.warehouse
                granary = village.granary
                if resources[account.LUMBER]/warehouse > warning_percent:
                    to_show = True
                    msg += '{} is over {}/{}\n'.format(
                        account.RESOURCE_TYPES[account.LUMBER],
                        resources[account.LUMBER],
                        warehouse)
                if resources[account.CLAY]/warehouse > warning_percent:
                    msg += '{} is over {}/{}\n'.format(
                        account.RESOURCE_TYPES[account.CLAY],
                        resources[account.CLAY],
                        warehouse)
                if resources[account.IRON]/warehouse > warning_percent:
                    to_show = True
                    msg += '{} is over {}/{}\n'.format(
                        account.RESOURCE_TYPES[account.IRON],
                        resources[account.IRON],
                        warehouse)
                if resources[account.CROP]/granary > warning_percent:
                    to_show = True
                    msg += '{} is over {}/{}\n'.format(
                        account.RESOURCE_TYPES[account.CROP],
                        resources[account.CROP],
                        granary)
            if to_show:
                notification = notify2.Notification(title, msg)
                notification.show()
            time.sleep(10 + 20 * random.random())

watcher = Watcher()
watcher.watch()
