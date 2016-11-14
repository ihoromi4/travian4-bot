import logging
import time
import re

import requests
import bs4

logging.debug('Start loading travlib/loging.py')

class LoginError(Exception):
    pass


class HashableDict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))


class Login:
    def __init__(self, url_data, name, password, headers={}):
        self.url_data = url_data
        self.server_url = self.url_data["server-url"]
        self.name = name
        self.password = password
        self.headers = headers
        self.session = requests.Session()
        self.relogin_delay = 0.33
        self.reconnections = 3
        self.html_obsolescence_time = 0.33
        self.loggedin = False
        self.html_sources = dict()
        self._game_version = None

    def send_request(self, url, data={}, params={}):
        try:
            if len(data) == 0:
                logging.debug('Send get request to url: {}'.format(url))
                html = self.session.get(url, headers=self.headers, params=params)
                # html = self.session.request('GET', url, headers=self.headers, data=data, params=params, cookies, allow_redirects=True)
            else:
                logging.debug('Send post request to url: {}'.format(url))
                html = self.session.post(url, headers=self.headers, data=data)
        except:
            logging.error('Net problem, cant fetch the URL {}'.format(url))
            print('Net problem, cant fetch the URL' + url)
            raise
        return html

    def login(self):
        print('Start Login')
        html = self.send_request(self.server_url)
        # start parse
        parser = bs4.BeautifulSoup(html.text, 'html5lib')
        s1 = parser.find('button', {'name': 's1'})['value'].encode('utf-8')
        login = parser.find('input', {'name': 'login'})['value']
        # start login
        data = {
            'name': self.name,
            'password': self.password,
            's1': s1,
            'w': '1366:768',
            'login': login
            }
        html = self.send_request(self.server_url + '/dorf1.php', data=data)
        if 'playerName' in html.text:
            self.loggedin = True
            print('Login succeed!')
            return True
        self.loggedin = False
        print('Login fail!')
        return False

    def load_page(self, url, data={}):
        if not self.loggedin:
            if not self.login():
                raise LoginError("Something is wrong.")
        html = self.send_request(url, data)
        if 'playerName' not in html.text:
            self.loggedin = False
            print('Suddenly logged off')
            for i in range(self.reconnections):
                if self.login():
                    html = self.send_request(url, data)
                    return html
                else:
                    print(('Could not relogin %d time' % (self.reconnections-i)))
                    time.sleep(self.relogin_delay)
        return html

    def get_html_source(self, url, data={}):
        key = (url, hash(tuple(sorted(data.items()))))
        if key in self.html_sources:
            html_source, load_time = self.html_sources[key]
            if time.time() - load_time < self.html_obsolescence_time:
                return html_source
        load_time = time.time()
        html_source = self.load_page(url, data)
        self.html_sources[key] = (html_source, load_time)
        return html_source

    def load_dorf1(self, village_id):
        return self.get_html_source(self.server_url + '/dorf1.php?newdid={}&'.format(village_id))

    def get_game_version(self):
        if not self._game_version:
            html = self.get_html_source(self.server_url + '/dorf1.php').text
            pattern = r"Travian.Game.version = '([.\d]*)';"
            regex = re.compile(pattern)
            results = regex.findall(html)
            if not len(results):
                raise TypeError("It is not travian page!")
            try:
                game_version = float(results[0])
            except ValueError:
                raise ValueError("Bad parsing pattern!")
            self._game_version = game_version
        return self._game_version
    game_version = property(get_game_version)

logging.debug('Start loading travlib/loging.py')
