import re

import bs4

from .village import Village
from . import buildings

NATIONS = ['romans', 'teutons', 'gauls']

RESOURCE_TYPES = ['lumber', 'clay', 'iron', 'crop']
LUMBER = 0
CLAY = 1
IRON = 2
CROP = 3


class Account:
    def __init__(self, login):
        self.login = login
        self.langdata = login.langdata
        self._villages = {}  # id: village
        self.nation = NATIONS[self.nation_id-1]
        self.update_villages()

    def get_nation_id(self):
        html = self.login.get_html("dorf1.php")
        nation_compile = re.compile('nation(\d)')
        nation = nation_compile.findall(html)[0]
        return int(nation)
    nation_id = property(get_nation_id)

    def get_village_ids(self):
        html = self.login.get_html("dorf1.php")
        pattern = r'<a  href="\?newdid=(\d+)&amp;"'
        village_village_ids_compile = re.compile(pattern)
        village_village_ids = village_village_ids_compile.findall(html)
        village_village_ids = [int(id) for id in village_village_ids]
        return village_village_ids

    def update_villages(self):
        village_ids = self.get_village_ids()
        village_positions = self.get_villages_positions()
        for id in village_ids:
            if id not in self._villages:
                pos = village_positions[village_ids.index(id)]
                village = Village(self, id, pos)
                self._villages[id] = village

    def get_villages(self) -> Village:
        return list(self._villages.values())
    villages = property(get_villages)

    def get_villages_amount(self):
        self.update_villages()
        return len(self._villages)
    villages_amount = property(get_villages_amount)

    def get_villages_names(self):
        html = self.login.get_html("dorf1.php")
        pattern = r'<div class="name">(.*)</div>'
        regex = re.compile(pattern)
        names = regex.findall(html)
        return names
    villages_names = property(get_villages_names)

    def get_ajax_token(self):
        html = self.login.get_html("dorf1.php")
        pattern = r'ajaxToken\s*=\s*\'(\w+)\''
        ajax_token_compile = re.compile(pattern)
        ajax_token = ajax_token_compile.findall(html)[0]
        return ajax_token
    ajax_token = property(get_ajax_token)

    def get_villages_positions(self):
        html = self.login.get_html("dorf1.php")
        pattern = r'coordinateX">\(&#x202d;&(#45;)*&*#x202d;(\d+)'
        x_compile = re.compile(pattern)
        x = x_compile.findall(html)
        pattern = r'coordinateY">&#x202d;&(#45;)*&*#x202d;(\d+)'
        y_compile = re.compile(pattern)
        y = y_compile.findall(html)
        positions = []
        for i in range(len(x)):
            position = [0, 0]
            if '#45' in x[i][0]:
                position[0] = -int(x[i][1])
            else:
                position[0] = int(x[i][1])
            if '#45' in y[i][0]:
                position[1] = -int(y[i][1])
            else:
                position[1] = int(y[i][1])
                positions.append(position)
        return positions
    villages_positions = property(get_villages_positions)

    def get_village_by_name(self, name: str):
        for village in self.villages:
            if village.name == name:
                return village
        return None

    def get_gold(self):
        html = self.login.get_html("dorf1.php")
        soup = bs4.BeautifulSoup(html, 'html5lib')
        gold_silver_cintainer = soup.find('div', {'id': 'goldSilverContainer'})
        gold_container = gold_silver_cintainer.find('div', {'class': 'gold'})
        gold_span = gold_container.find('span', {'class': 'ajaxReplaceableGoldAmount'})
        return int(gold_span.text)
    gold = property(get_gold)

    def get_silver(self):
        html = self.login.get_html("dorf1.php")
        soup = bs4.BeautifulSoup(html, 'html5lib')
        gold_silver_cintainer = soup.find('div', {'id': 'goldSilverContainer'})
        silver_container = gold_silver_cintainer.find('div', {'class': 'silver'})
        silver_span = silver_container.find('span', {'class': 'ajaxReplaceableSilverAmount'})
        return int(silver_span.text)
    silver = property(get_silver)