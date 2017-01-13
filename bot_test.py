from travlib import account

url = 'http://ts70.travian.com/'
name = 'bro'
password = '2bd384f'

# url = 'http://ts5.travian.ru/'
# name = 'broo'
# password = 'wA4iN_tYR'

acc = account.Account(url, name, password)

print(acc.map.get_area((-55, -20)))
