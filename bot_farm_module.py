import time
import configparser
import json

from travlib import account

config = configparser.ConfigParser()
config.read('config.ini')

url = 'http://ts70.travian.com/'
name = 'bro'
password = '2bd384f'

user_agent = config['HEADERS']['user_agent']
headers = {'User-Agent': user_agent}

acc = account.Account(url, name, password, headers)


def bot_attack_raid():
    import time

    from botlib import farmservice

    village = acc.get_village_by_id(69437)
    print('Village:', village.name)

    with open('data/servers/ts70/farm.json') as file:
        json_data = json.load(file)

    farms = json_data['farms']

    farming = farmservice.FarmService(village, farms)

    while True:
        farming.update()
        time.sleep(1)

while True:
    try:
        bot_attack_raid()
    except BaseException as e:
        print(e)
        raise
    time.sleep(20 * 60)
