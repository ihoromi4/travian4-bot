import configparser
import json

from travlib import login
from travlib import account

config = configparser.ConfigParser()
config.read('config.ini')

server_url = config['URL']['server_url']
login_url = config['URL']['login_url'].replace('{server_url}', server_url)

name = config['USER']['name']
password = config['USER']['password']

user_agent = config['HEADERS']['user_agent']
headers = {'User-Agent': user_agent}

with open('data/url.json', 'r') as stream:
    url_data = json.load(stream)['ts5ru']

login_ = login.Login(url_data, name, password, headers)
print('Travian version:', login_.game_version)

account_ = account.Account(login_)

print(account_.get_village_ids())

village1 = account_.villages[0]
village2 = account_.villages[1]
print(village2.get_builds())
print(village2.outside.get_buildings())
'''
print('village 1 id:', village1.id)
print('name village 1:', village1.name)
print('warehouse:', village1.get_warehouse())
print('granary:', village1.get_granary())
print('get_resources:', village1.get_resources())
print('get_production:', village1.get_production())

print('village 2 id:', village2.id)
print('name village 2:', village2.name)
print('warehouse:', village2.get_warehouse())
print('granary:', village2.get_granary())
print('get_resources:', village2.get_resources())
print('get_production:', village2.get_production())
'''