import configparser
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

login()
