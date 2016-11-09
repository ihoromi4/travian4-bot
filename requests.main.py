import configparser
import re

import requests
from bs4 import BeautifulSoup

config = configparser.ConfigParser()
config.read('config.ini')

server_url = config['URL']['server_url']
login_url = config['URL']['login_url'].replace('{server_url}', server_url)

name = config['USER']['name']
password = config['USER']['password']

user_agent = config['HEADERS']['user_agent']
headers = {'User-Agent' : user_agent}

session = requests.Session()

def send_request(url, data={}):
    try:
        if len(data) == 0:
            html = session.get(url, headers=headers)
        else:
            html = session.post(url, headers=headers, data=data)
    except:
        raise
    return html.text

def get_info(html):
    village_vids_compile = re.compile('\?newdid=(\d+)')
    village_vids = village_vids_compile.findall(html)
    print('vids', village_vids)
    village_amount = len(village_vids)
    print('amount', village_amount)
    nation_compile = re.compile('nation(\d)')
    nation = nation_compile.findall(html)[0]
    print('nation', nation)
    x_compile = re.compile('coordinateX">\(&#x202d;&(#45;)*&*#x202d;(\d+)')
    X = x_compile.findall(html)
    y_compile = re.compile('coordinateY">&#x202d;&(#45;)*&*#x202d;(\d+)')
    Y = y_compile.findall(html)
    pos = []
    for i in range(len(X)):
        p = [0, 0]
        if '#45' in X[i][0]:
            p[0] = -int(X[i][1])
        else:
            p[0] = int(X[i][1])
        if '#45' in Y[i][0]:
            p[1] = -int(Y[i][1])
        else:
            p[1] = int(Y[i][1])
        pos.append(p)
    print('pos', pos)
    ajax_token_compile = re.compile('ajaxToken\s*=\s*\'(\w+)\'')
    ajax_token = ajax_token_compile.findall(html)[0]
    print('ajax token', ajax_token)

def login():
    print('Start Login')
    html = send_request(server_url)
    parser = BeautifulSoup(html, 'html5lib')
    s1 = parser.find('button', {'name':'s1'})['value'].encode('utf-8')
    login = parser.find('input', {'name':'login'})['value']
    # start login
    data = {
        'name' : name,
        'password' : password,
        's1' : s1,
        'w' : '1366:768',
        'login' : login
        }
    html = send_request(server_url + '/dorf1.php', data)
    if html != False:
        print('successed!')
        get_info(html)

login()
