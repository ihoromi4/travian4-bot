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

print(account_.gold)
print(account_.silver)
# village1 = account_.get_village_by_name('3.Сахар')
# print(village1.name)
# print(village1.builds)
