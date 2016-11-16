import configparser

from travlib import login
from travlib import account
from travlib import language

config = configparser.ConfigParser()
config.read('config.ini')

name = 'broo'
password = '1994igor'

user_agent = config['HEADERS']['user_agent']
headers = {'User-Agent': user_agent}

lang = language.Language('data/language.json', 'ru', 'ts5')

logn = login.Login(lang, name, password, headers)
print('Travian version:', logn.game_version)

account_ = account.Account(logn)

village1 = account_.villages[0]
village2 = account_.villages[1]

marketplace = village1.inside.marketplace
if marketplace:
    print(marketplace.name, marketplace.level)
    print(marketplace.get_pages())
else:
    print("No marketplace")
