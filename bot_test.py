from travlib import account
from travlib import map

url = 'http://ts70.travian.com/'
name = 'bro'
password = '2bd384f'

url = 'http://ts5.travian.ru/'
name = 'broo'
password = 'wA4iN_tYR'

acc = account.Account(url, name, password)

# v = acc.get_village_by_id(79385) # 1
v = acc.get_village_by_id(84821)  # 2

print(v.resources)
