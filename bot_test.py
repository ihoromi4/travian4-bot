from travlib import account
from travlib import map

url = 'http://ts70.travian.com/'
name = 'bro'
password = '2bd384f'

# url = 'http://ts5.travian.ru/'
# name = 'broo'
# password = 'wA4iN_tYR'

acc = account.Account(url, name, password)

#area = acc.map.get_area((-55, -20), map.Zoom.MAX)
print(acc.map.get_pos_info((-56, -18)))
