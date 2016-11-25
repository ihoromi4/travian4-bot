import configparser

from travlib import login
from travlib import account
from travlib import language

config = configparser.ConfigParser()
config.read('config.ini')

lang_dir = 'data/language/'
url = 'http://ts5.travian.ru/'
name = 'broo'
password = '1994igor'

user_agent = config['HEADERS']['user_agent']
headers = {'User-Agent': user_agent}

logn = login.Login(lang_dir, url, name, password, headers)
print('Travian version:', logn.game_version)
print('Server language:', logn.language)

account_ = account.Account(logn)

village1 = account_.villages[0]
village2 = account_.villages[1]
village3 = account_.villages[2]
print(village1.name)
marketplace = village1.inside.marketplace
marketplace.send_resources((-80, 93), (2000, 500, 1000, 0))
