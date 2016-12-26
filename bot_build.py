import configparser

from travlib import account

from botlib import bot

'''
Задача:
    Реализовать систему автономной застройки ресурсных полей.
'''

url = 'http://ts70.travian.com/'
name = 'bro'
password = '2bd384f'

# url = 'http://ts5.travian.ru/'
# name = 'broo'
# password = '1994igor'

user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'
headers = {'User-Agent': user_agent}

acc = account.Account(url, name, password, headers)

builder = bot.ResourceBuilder(acc)
builder.resource_balance_builder()

# print(acc.reports.get_offensive_reports())
# acc.reports.mark_readed_report(21853776)

# acc.reports.mark_as_read_all()

# acc.reports.clear()
