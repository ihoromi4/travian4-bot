import configparser

from travlib import login
from travlib import account

config = configparser.ConfigParser()
config.read('config.ini')

server_url = config['URL']['server_url']
login_url = config['URL']['login_url'].replace('{server_url}', server_url)

name = config['USER']['name']
password = config['USER']['password']

user_agent = config['HEADERS']['user_agent']
headers = {'User-Agent' : user_agent}

login_ = login.Login(server_url, name, password, headers)
#login_.login()
login_.load_dorf1(79385)

#account_ = account.Account(login_)
#print(account_.get_info())
#print(account_.get_village_ids())
#print(account_.get_village_names())
#print(account_.get_resources())

