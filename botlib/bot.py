from travlib import account
from travlib.village.buildings import resourcefield


class ResourceBuilder:
    def __init__(self, account: account.Account):
        self.account = account

    def error_test(self):
        import time
        village = self.account.villages[0]
        print(village.name)
        print(village.builds)
        print('sleep')
        time.sleep(600)
        print(village.builds)

    def outside_build(self):
        import time
        import random

        village = self.account.villages[0]
        print(village.name)
        print(village.builds)

        def get_low_level_build():
            buildings = village.outer.buildings
            building = buildings[0]
            for b in buildings:
                if not type(b) is resourcefield.Cropland:
                    if b.level < building.level:
                        building = b
            return building

        def get_low_level_cropland():
            buildings = village.outer.buildings
            building = buildings[0]
            for b in buildings:
                if type(b) is resourcefield.Cropland:
                    if b.level < building.level:
                        building = b
            return building

        while True:
            if not village.builds:
                if village.free_crop >= 5:
                    building = get_low_level_build()
                    building.build()
                else:
                    building = get_low_level_cropland()
                    building.build()
            print('sleep')
            time.sleep(60 + 240 * random.random())
