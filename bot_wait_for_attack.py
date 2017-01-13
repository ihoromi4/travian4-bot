import time
import random
import configparser

from guilib import push

from travlib import account

config = configparser.ConfigParser()
config.read('config.ini')

user_agent = config['HEADERS']['user_agent']
headers = {'User-Agent': user_agent}

pushbullet_api_key = config['PUSHBULLET']['api_key']
push.init(pushbullet_api_key)

url = 'http://ts70.travian.com/'
name = 'bro'
password = '2bd384f'

url = 'http://ts5.travian.ru/'
name = 'broo'
password = 'wA4iN_tYR'

acc = account.Account(url, name, password, headers)

SLEEP = 2 * 60


def watcher():
    attacks = dict()
    while True:
        for village in acc.villages:
            movements = village.troops.get_movements()
            if 'in-attack' in movements:
                in_attack = movements['in-attack']
                number = in_attack['number']
                if attacks.get(village.id, 0) < number:
                    push.send('Incoming attack!', 'Begin attack on village: {}'.format(village.name))
                attacks[village.id] = number
            else:
                attacks[village.id] = 0
        time.sleep(SLEEP/2 + SLEEP * random.random())

watcher()
