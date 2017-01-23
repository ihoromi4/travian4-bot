import time
import random

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


class VillageTransfer:
    def __init__(self, village, setting: dict={}):
        self.village = village
        self.type = setting['type']

    def update(self):
        marketplace = self.village.get_building('marketplace')
        if self.type == TARGET:
            print('target wait')
            return
        if marketplace.free_merchants == 0:
            print('source no free merchants')
            return
        print('source send')


class ResourceTransfer:
    def __init__(self, account: account.Account, settings: dict={}):
        self.transfers = []
        for id in settings:
            village = account.get_village_by_id(id)
            tr = VillageTransfer(village, settings[id])
            self.transfers.append(tr)

    def update(self):
        for transfer in self.transfers:
            transfer.update()


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


transfer = ResourceTransfer(acc, settings)
transfer.update()
