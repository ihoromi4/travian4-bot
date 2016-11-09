import configparser

import login

config = configparser.ConfigParser()
config.read('config.ini')

server_url = config['URL']['server_url']
login_url = config['URL']['login_url'].replace('{server_url}', server_url)

name = config['USER']['name']
password = config['USER']['password']

user_agent = config['HEADERS']['user_agent']
headers = {'User-Agent' : user_agent}

login_ = login.Login(server_url, name, password, headers)
login_.login()
