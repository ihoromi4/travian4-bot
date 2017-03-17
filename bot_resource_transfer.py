import time
import random

import logging

from travlib import account

url = 'http://ts5.travian.ru/'
name = 'broo'
password = 'wA4iN_tYR'

user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'
headers = {'User-Agent': user_agent}

acc = account.Account(url, name, password, headers)

TARGET = 1
SOURCE = 2

settings = {
    79385: {'type': TARGET},  # 1.
    84821: {'type': TARGET},
    86917: {'type': SOURCE},
    88380: {'type': SOURCE},
    89791: {'type': SOURCE},
    90902: {'type': SOURCE},
    91726: {'type': SOURCE},
    92436: {'type': SOURCE}
}


class ResourceTransferNode:
    def __init__(self, village, setting: dict={}):
        self.village = village
        self.type = setting['type']

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

    def act_target(self):
        logging.debug('target wait')

    def act_source(self):
        if not self.marketplace:
            # в деревне нет рынка
            return
        if self.marketplace.free_merchants == 0:
            # на рынке нет свободных торговцев
            logging.debug('на рынке нет свободных торговцев')
            return

        capacity = self.able_carry * self.marketplace.free_merchants
        max_resource = self.village.warehouse
        limit_resource = 0.2 * max_resource
        resources = self.village.resources
        resources[3] = 0
        free_resources = [max(0, r - limit_resource) for r in resources]

        if capacity < sum(free_resources):
            factor = capacity / sum(free_resources)
            free_resources = [int(r * factor) for r in free_resources]

        transfer_target = (-80, 92)
        transfer_task = free_resources

        self.marketplace.send_resources(transfer_target, transfer_task)

        logging.debug('ресурсы отправлены')

    def update(self):
        if self.type == TARGET:
            self.act_target()
        elif self.type == SOURCE:
            self.act_source()


class ResourceTransferNet:
    def __init__(self, account: account.Account, settings: dict={}):
        self.nodes = []
        for id in settings:
            village = account.get_village_by_id(id)
            node = ResourceTransferNode(village, settings[id])
            self.nodes.append(node)

    def update(self):
        for node in self.nodes:
            node.update()
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
