import bs4

from . import building


# Точка сбора
class RallyPoint(building.Building):
    def __init__(self, village_part, name, id, level):
        building.Building.__init__(self, village_part, name, id, level)
        self.eng_name = 'rallypoint'

    def post(self, url, params, data):
        pass

    def reinforcement(self):
        pass

    def attack_normal(self):
        pass

    def attack_raid(self, pos):
        pass

    def step_1(self, pos, c=4):
        send_troops_page = 2
        html = self.village_part.village.login.get_html('build.php', {'id': self.id, 'tt': send_troops_page})
        soup = bs4.BeautifulSoup(html, 'html5lib')
        div_build = soup.find('div', {'id': 'build'})
        data = dict()
        data['x'] = pos[0]
        data['y'] = pos[1]
        data['c'] = c
        data['timestamp'] = div_build.find('input', {'name': 'timestamp'})['value']
        data['timestamp_checksum'] = div_build.find('input', {'name': 'timestamp_checksum'})['value']
        data['b'] = div_build.find('input', {'name': 'b'})['value']
        data['currentDid'] = div_build.find('input', {'name': 'currentDid'})['value']
        self.step_2(data)

    def step_2(self, data):
        send_troops_page = 2
        params = {'id': self.id, 'tt': send_troops_page}
        data_ = {
            'redeployHero': '',
            'timestamp': 0,
            'timestamp_checksum': 0,
            'id': '1',
            'a': 'aaa',
            'c': 0,
            'kid': '343',
            't1': '0',
            't5': 5,
            't11': '0',
            'sendReally': '0',
            'troopsSent': '1',
            'currentDid': 0,
            'b': 0,
            'dname': '',
            'x': 0,
            'y': 0,
            's1': 'ok'
        }
        data['t5'] = 5
        data['s1'] = 'ok'

        self.step_3(data)

    def step_3(self, data):
        send_troops_page = 2
        params = {'id': self.id, 'tt': send_troops_page}
        html = self.village_part.village.login.server_post('build.php', data=data, params=params)
        soup = bs4.BeautifulSoup(html, 'html5lib')
        div_build = soup.find('div', {'id': 'build'})
        # data = {}
        data['timestamp'] = div_build.find('input', {'name': 'timestamp'})['value']
        data['timestamp_checksum'] = div_build.find('input', {'name': 'timestamp_checksum'})['value']
        data['id'] = div_build.find('input', {'name': 'id'})['value']
        data['a'] = div_build.find('input', {'name': 'a'})['value']
        data['c'] = div_build.find('input', {'name': 'c'})['value']
        data['kid'] = div_build.find('input', {'name': 'kid'})['value']
        for i in range(1, 12):
            data['t%s' % (i,)] = div_build.find('input', {'name': 't%s' % (i,)})['value']
        data['sendReally'] = div_build.find('input', {'name': 'sendReally'})['value']
        data['troopsSent'] = div_build.find('input', {'name': 'troopsSent'})['value']
        data['currentDid'] = div_build.find('input', {'name': 'currentDid'})['value']
        data['b'] = div_build.find('input', {'name': 'b'})['value']
        data['dname'] = div_build.find('input', {'name': 'dname'})['value']
        data['x'] = div_build.find('input', {'name': 'x'})['value']
        data['y'] = div_build.find('input', {'name': 'y'})['value']
        html = self.village_part.village.login.server_post('build.php', data=data, params=params)

    def send_troops(self, pos, c=4):
        # c = 2       # Reinforcement
        # c = 3       # Attack: Normal
        # c = 4       # Attack: Raid
        print(self.village_part.village.name, 'raid to', pos)
        troops_type = 't5'
        self.step_1(pos, c)
