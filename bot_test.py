from travlib import account
from travlib import map

url = 'http://ts70.travian.com/'
name = 'bro'
password = '2bd384f'

url = 'http://ts5.travian.ru/'
name = 'broo'
password = 'wA4iN_tYR'

acc = account.Account(url, name, password)

for village in acc.villages:
    tradeoffice = village.get_building('tradeoffice')
    if tradeoffice:
        able_carry = tradeoffice.able_carry
    else:
        able_carry = 750
    print('name: ', village.name, ', able carry:', able_carry)
