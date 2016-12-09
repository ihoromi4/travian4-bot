import configparser

from travlib import account
from travlib import login
from travlib.village.buildings import resourcefield

config = configparser.ConfigParser()
config.read('config.ini')

lang_dir = 'data/language/'
url = 'http://ts70.travian.com/'
name = 'bro'
password = '2bd384f'

# ru
# url = 'http://ts5.travian.ru/'
# name = 'broo'
# password = '1994igor'

user_agent = config['HEADERS']['user_agent']
headers = {'User-Agent': user_agent}

logn = login.Login(lang_dir, url, name, password, headers)
print('Travian version:', logn.game_version)
print('Server language:', logn.language)


account_ = account.Account(logn)

village = account_.villages[0]
print(village.name)
print(village.builds)


def outside_build():
    import time
    import random
    while True:
        if not village.builds:
            if village.free_crop >= 5:
                for building in village.outside.buildings:
                    if building.level == 2 and not type(building) is resourcefield.Cropland:
                        building.build()
                        break
            else:
                for building in village.outside.buildings:
                    if building.level == 1 and type(building) is resourcefield.Cropland:
                        building.build()
                        break
        time.sleep(60 + 60 * random.random())

# outside_build()
