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

user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'
headers = {'User-Agent': user_agent}

acc = account.Account(url, name, password, headers)

builder = bot.ResourceBuilder(acc)
builder.error_test()
