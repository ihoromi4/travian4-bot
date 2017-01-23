from travlib import account
from travlib import map

url = 'http://ts70.travian.com/'
name = 'bro'
password = '2bd384f'

# url = 'http://ts5.travian.ru/'
# name = 'broo'
# password = 'wA4iN_tYR'

acc = account.Account(url, name, password)

for v in acc.villages:
    print(v.name)

village = acc.villages[0]

marketplace = village.get_building('marketplace')
print('m:', marketplace.free_merchants)
