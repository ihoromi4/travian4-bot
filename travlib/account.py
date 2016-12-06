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

    def update_villages(self):
        villages_data = self.read_villages_data()
        for vdata in villages_data:
            id = vdata['id']
            pos = vdata['coords']
            if id not in self._villages:
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

    def read_villages_data(self):
        html = self.login.get_html("dorf1.php")
        soup = bs4.BeautifulSoup(html, 'html5lib')
        div = soup.find('div', {'id': 'sidebarBoxVillagelist'})
        inner_box = div.find('div', {'class': 'innerBox content'})
        all_li = inner_box.find_all('li')
        villages_data = []
        for li in all_li:
            village = {}
            href = li.find('a')['href']
            id = int(re.findall(r'id=(\d+)&', href)[0])
            village['id'] = id

            div_name = li.find('div', {'class': 'name'})
            name = div_name.text
            village['name'] = name

            strip = lambda x: x.replace('\u202d', '').replace('\u202c', '').strip('()')
            span_x = li.find('span', {'class': 'coordinateX'})
            x = int(strip(span_x.text))
            span_y = li.find('span', {'class': 'coordinateY'})
            y = int(strip(span_y.text))
            village['coords'] = (x, y)
            villages_data.append(village)
        return villages_data

    def read_spieler(self):
        html = self.login.get_html("spieler.php")
        soup = bs4.BeautifulSoup(html, 'html5lib')
        table = soup.find('table', {'id': 'villages'})
        table_body = table.find('tbody')
        all_tr = table_body.find_all('tr')
        villages_data = []
        for tr in all_tr:
            village = {}
            name_td = tr.find('td', {'class': 'name'})
            name_a = name_td.find('a')
            village_name = name_a.text
            village['name'] = village_name
            name_span_capital = name_td.find('span', {'class': 'mainVillage'})
            is_capital = bool(name_span_capital)
            village['is_capital'] = is_capital

            oases_td = tr.find('td', {'class': 'oases merged'})

            inhabitants_td = tr.find('td', {'class': 'inhabitants'})
            inhabitants = int(inhabitants_td.text)
            village['inhabitants'] = inhabitants

            coords_td = tr.find('td', {'class': 'coords'})
            span_x = coords_td.find('span', {'class': 'coordinateX'})
            strip = lambda x: x.replace('\u202d', '').replace('\u202c', '').strip('()')
            x = int(strip(span_x.text))
            span_y = coords_td.find('span', {'class': 'coordinateY'})
            y = int(strip(span_y.text))
            village['coords'] = (x, y)
            villages_data.append(village)
        return villages_data

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