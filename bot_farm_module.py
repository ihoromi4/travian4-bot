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
url = 'http://ts5.travian.ru/'
name = 'broo'
password = 'wA4iN_tYR'

user_agent = config['HEADERS']['user_agent']
headers = {'User-Agent': user_agent}

acc = account.Account(url, name, password, headers)


def print_info():
    print('Travian version:', acc.login.game_version)
    print('Server language:', acc.login.server_language)
    print('Server time:', acc.server_time)

    print('Rank:', acc.rank)
    print('Alliance:', acc.alliance)
    print('Villages amount:', acc.villages_amount)
    print('Population:', acc.population)
    print(acc.villages)

# print_info()


def bot_attack_raid():
    import time

    from botlib import farmservice

    village = acc.get_village_by_id(79385)
    print('Village:', village.name)

    farms = {
        (-83, 89),
        (-79, 93),
        (-70, 89),
        (-87, 89),
        (-72, 93),
        (-76, 86),
        (-77, 99),
        (-79, 99),
        (-81, 89),
        (-86, 82),
        # (-74, 86)
    }

    farming = farmservice.FarmService(village, farms)

    while True:
        farming.update()
        time.sleep(1)

bot_attack_raid()
'''
Фарм - обнаружена проблемма!
Если войск меньше, чем указано, то отправляется доступное количество.
Должно быть: отправляется указанное количество, или ничего.
'''
