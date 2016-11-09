import requests
import bs4 # BeautifulSoup

class Login:
    def __init__(self, server_url, name, password, headers):
        self.server_url = server_url
        self.name = name
        self.password = password
        self.headers = headers
        self.session = requests.Session()

    def send_request(self, url, data={}):
        try:
            if len(data) == 0:
                html = self.session.get(url, headers=self.headers)
            else:
                html = self.session.post(url, headers=self.headers, data=data)
        except:
            raise
        return html.text

    def login(self):
        print('Start Login')
        html = self.send_request(self.server_url)
        parser = bs4.BeautifulSoup(html, 'html5lib')
        s1 = parser.find('button', {'name':'s1'})['value'].encode('utf-8')
        login = parser.find('input', {'name':'login'})['value']
        # start login
        data = {
            'name' : self.name,
            'password' : self.password,
            's1' : s1,
            'w' : '1366:768',
            'login' : login
            }
        html = self.send_request(self.server_url + '/dorf1.php', data)
        if html != False:
            print('successed!')

