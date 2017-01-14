import time
import random
import configparser

from travlib import account

from botlib import overwatch

config = configparser.ConfigParser()
config.read('config.ini')

user_agent = config['HEADERS']['user_agent']
headers = {'User-Agent': user_agent}

pushbullet_api_key = config['PUSHBULLET']['api_key']

url = 'http://ts70.travian.com/'
name = 'bro'
password = '2bd384f'

url = 'http://ts5.travian.ru/'
name = 'broo'
password = 'wA4iN_tYR'

acc = account.Account(url, name, password, headers)

watch = overwatch.Overwatch(acc)
watch.add_pushbullet(pushbullet_api_key)
watch.on_attack = lambda: print('attack!')

SLEEP = 2 * 60


def watcher():
    while True:
        watch.inspect()
        time.sleep(SLEEP/2 + SLEEP * random.random())

watcher()
