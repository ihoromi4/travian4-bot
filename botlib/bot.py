import time
import random

from travlib import account
from travlib.village.buildings import resourcefield

BUILDINGS_TYPES = [
    resourcefield.Woodcutter,
    resourcefield.Claypit,
    resourcefield.Ironmine,
    resourcefield.Cropland
]


class ResourceBuilder:
    def __init__(self, account: account.Account):
        self.account = account

    def error_test(self):
        village = self.account.villages[0]
        print(village.name)
        print(village.builds)
        print('sleep')
        time.sleep(600)
        print(village.builds)

    @staticmethod
    def get_low_level_build(village, building_type=None):
        buildings = village.outer.buildings
        building = None
        for b in buildings:
            if not building:
                if not building_type:
                    building = b
                elif type(b) is building_type:
                    building = b
            else:
                if type(b) is building_type:
                    if b.level < building.level:
                        building = b
        return building

    def resource_balance_builder(self):
        village = self.account.villages[0]
        while True:
            if not village.builds:
                resources = village.resources
                min_res = min(resources[:3])
                min_res_index = resources.index(min_res)
                building_type = BUILDINGS_TYPES[min_res_index]
                if village.free_crop >= 5:
                    building = self.get_low_level_build(village, building_type)
                    building.build()
                else:
                    building = self.get_low_level_build(village, resourcefield.Cropland)
                    building.build()
            print('sleep')
            time.sleep(300 + 300 * random.random())

    def outside_build(self):
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
