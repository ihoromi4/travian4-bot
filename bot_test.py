from travlib import account

url = 'http://ts70.travian.com/'
name = 'bro'
password = '2bd384f'

acc = account.Account(url, name, password)

print(acc.villages)

village = acc.villages[0]
print(village.outer.buildings)
