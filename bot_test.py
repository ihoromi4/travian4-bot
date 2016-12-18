import configparser

from travlib import account
from travlib.village.buildings import resourcefield

config = configparser.ConfigParser()
config.read('config.ini')

url = 'http://ts70.travian.com/'
name = 'bro'
password = '2bd384f'

url = 'http://ts2.travian.com/'
name = 'bro'
password = '1994igor'

# ru
# url = 'http://ts5.travian.ru/'
# name = 'broo'
# password = '1994igor'

user_agent = config['HEADERS']['user_agent']
headers = {'User-Agent': user_agent}

acc = account.Account(url, name, password, headers)

print('Travian version:', acc.login.game_version)
print('Server language:', acc.login.server_language)
print('Server time:', acc.server_time)

print('Rank:', acc.rank)
print('Alliance:', acc.alliance)
print('Villages amount:', acc.villages_amount)
print('Population:', acc.population)

print(acc.villages)

village = acc.villages[0]
print(village.name)
print(village.builds)


def outside_build():
    import time
    import random

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

outside_build()
