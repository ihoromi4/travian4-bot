import json

import bs4

from .travparse import position_details


class Map:
    """ Реализация доступа к игровой карте """

    def __init__(self, account):
        self.account = account

    def get_pos_info(self, pos: list) -> dict:
        """ Возвращает информацию о указаной клетке """
        params = {'x': pos[0], 'y': pos[1]}
        html = self.account.login.server_get('position_details.php', params=params)
        soup = bs4.BeautifulSoup(html, 'html5lib')
        info = position_details.get_pos_info(soup)
        info['pos'] = pos
        return info

    def get_area(self, pos: list) -> dict:
        """ Возвращает информацию о всех клетках вокруг указаной. Быстрый метод """
        params = {'cmd': 'mapPositionData'}
        data = {
            'cmd': 'mapPositionData',
            'data[x]': pos[0],
            'data[y]': pos[1],
            'data[zoomLevel]': '1'
        }
        html = self.account.login.get_ajax(params=params, data=data)
        json_data = json.loads(html)['response']
        if json_data['error']:
            raise ValueError(json_data['errorMsg'])
        data = json_data['data']['tiles']
        info = []
        for elem in data:
            v = dict()
            v['pos'] = (int(elem['x']), int(elem['y']))
            v['d'] = int(elem.get('d', 0))  # dorf id, -1 for oasis, 0 for valley
            v['u'] = int(elem.get('u', -1))  # user id, nothing for oasis (now -1)
            v['a'] = int(elem.get('a', -1))  # alliance id, nothing for oasis (now -1)
            info.append(v)
        return info
