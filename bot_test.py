import configparser

from travlib import login
from travlib import account
from travlib import language

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
# village.outside.resource_fields[0].build()
# print(village1.builds)
