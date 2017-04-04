import time
import random
import logging
import requests

from travianapi import account

import travianbot
from travianbot import exceptions
from travianbot.web import interaction

url_api = 'http://igoromi4.pythonanywhere.com'
url_api = 'http://127.0.0.1:5000'

version_ok = interaction.verification(url_api, travianbot.__version_tuple__)
if not version_ok:
    print('Please, load new bot version')
    raise exceptions.VersionError()

accounts = interaction.load_accounts(url_api)

print('accounts:', accounts)

accounts = accounts[0]

url = accounts['url']  # 'http://ts5.travian.ru/'
name = accounts['username']  # 'broo'
password = accounts['password']  # 'wA4iN_tYR'

user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'
headers = {'User-Agent': user_agent}

acc = account.Account(url, name, password, headers)

# Типы поселений (битовые маски):
IGNORE = 0  # поселение игнорируется

DEVELOPMENT = 2**0  # поселение с ресурсными полями не максимального уровня
# в такие деревни поставляются ресурсы для застройки

BARRACKS = 2**1  # деревня производящая войска (нуждается в зерне)

RESOURCES = 2**2  # деревня производит ресурсы
CROP = 2**3  # дереня производит зерно

SOURCE = RESOURCES | CROP  # деревня производит и ресурсы и зерно

TARGET = DEVELOPMENT | BARRACKS  # требует ресурсов для построек и войск

settings = {
    79385: {'type': TARGET, 'priory': 1},  # 1.
    84821: {'type': TARGET, 'priory': 2},  # 2.
    86917: {'type': SOURCE, 'priory': 10},  # 3.
    88380: {'type': SOURCE, 'priory': 10},  # 4.
    89791: {'type': SOURCE, 'priory': 10},  # 5.
    90902: {'type': SOURCE, 'priory': 10},  # 6.
    91726: {'type': SOURCE, 'priory': 10},  # 7.
    92436: {'type': SOURCE, 'priory': 10},  # 8.
    93405: {'type': TARGET, 'priory': 3},  # 9.
    94524: {'type': TARGET, 'priory': 3},  # 10.
    95147: {'type': TARGET, 'priory': 3},  # 11.
    95965: {'type': TARGET, 'priory': 0},  # 12.
    96741: {'type': TARGET, 'priory': 0}  # 13.
}


class ResourceTransferNode:
    def __init__(self, village, setting: dict = {}):
        self.village = village
        self.type = setting['type']
        self.priory = setting['priory']

    def get_marketplace(self):
        return self.village.get_building('marketplace')

    marketplace = property(get_marketplace)

    def get_tradeoffice(self):
        return self.village.get_building('tradeoffice')

    tradeoffice = property(get_tradeoffice)

    def get_able_carry(self):
        if self.tradeoffice:
            return self.tradeoffice.able_carry
        else:
            return 500

    able_carry = property(get_able_carry)

    def need_resources(self):
        max_resource = self.village.warehouse
        max_crop = self.village.granary
        resources = self.village.resources
        production = self.village.production
        production_time = 1
        if self.marketplace:
            moves = self.marketplace.get_merchants_moves()
            moves_incoming = moves['incoming']
            move_resources = [move['resources'] for move in moves_incoming]
        else:
            return [0] * 4

        max_resources = [max_resource] * 3 + [max_crop]
        needs = [(max_resources[i] - resources[i]) for i in range(4)]

        needs = [(needs[i] - max(0, production[i]) * production_time) for i in range(4)]

        for move in move_resources:
            needs = [(needs[i] - move[i]) for i in range(4)]

        needs = [max(0, int(r)) for r in needs]

        print('needs:', needs)

        return needs

    def is_need_resources(self):
        return sum(self.need_resources()) > 0

    def send(self, target):
        if not self.marketplace:
            # в деревне нет рынка
            return
        if self.marketplace.free_merchants == 0:
            # на рынке нет свободных торговцев
            logging.debug('на рынке нет свободных торговцев')
            return

        capacity = self.able_carry * self.marketplace.free_merchants
        warehouse = self.village.warehouse
        granary = self.village.granary
        limit_percent = 0.1
        max_resource = [warehouse] * 3 + [granary]
        resources = self.village.resources
        # resources[3] = 0
        free_resources = [max(0.0, resources[i] - max_resource[i] * limit_percent) for i in range(4)]

        if capacity < sum(free_resources):
            factor = capacity / sum(free_resources)
            free_resources = [int(r * factor) for r in free_resources]

        need_to_send = target.need_resources()
        print('need resources:', need_to_send)

        free_resources = [min(need_to_send[i], free_resources[i]) for i in range(4)]

        transfer_target = target.village.pos
        transfer_task = free_resources

        self.marketplace.send_resources(transfer_target, transfer_task)

        logging.debug('ресурсы отправлены')

        return True

    def send_to(self, targets):
        for node in targets:
            if node.is_need_resources():
                print('need resources')
                if self.send(node):
                    print('send resources')
                    return True


class ResourceTransferNet:
    def __init__(self, account: account.Account, settings: dict = {}):
        self.nodes = []
        for id in settings:
            village = account.get_village_by_id(id)
            node = ResourceTransferNode(village, settings[id])
            self.nodes.append(node)

    def update(self):
        targets = [node for node in self.nodes if node.type == TARGET]
        key = lambda x: x.priory
        targets.sort(key=key)
        sources = [node for node in self.nodes if node.type == SOURCE]
        for node in sources:
            node.send_to(targets)
            time.sleep(3.0)


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
                    # if resources[account.CROP] / granary > transfer_percent:
                    #    if village.inside.marketplace.free_merchants > 0:
                    #        marketplace.send_resources(target_village.pos, (0, 0, 0, 500))
                    #        print('send crop')
        print('while iteration', time.time())
        time.sleep(30 + 30 * random.random())


def start_transfer_loop():
    from time import sleep
    transfer_net = ResourceTransferNet(acc, settings)

    while True:
        logging.debug('Просмотр деревень...')
        transfer_net.update()
        sleep(60 * 5)


if __name__ == '__main__':
    start_transfer_loop()
