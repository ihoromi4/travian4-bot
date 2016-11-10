import re

from .village import Village

NATIONS = ['gauls', 'romans', 'teutons']

RESOURCE_TYPES = ['lumber', 'clay', 'iron', 'crop']
LUMBER = 0
CLAY = 1
IRON = 2
CROP = 3


class Account:
    def __init__(self, login):
        self.login = login
        self.villages = {}  # id: village

    def update_villages(self):
        village_ids = self.get_village_ids()
        for id in village_ids:
            if id not in self.villages:
                village = Village(self, id)
                self.villages[id] = village

    def get_info(self):
        info = dict()
        info['ajax_token'] = self.get_ajax_token()
        info['nation'] = self.get_nation()
        info['village_ids'] = self.get_village_ids()
        info['village_amount'] = self.get_village_amount()
        info['village_names'] = self.get_village_names()
        info['village_pos'] = self.get_village_pos()
        return info

    def get_ajax_token(self):
        html = self.login.login()
        pattern = r'ajaxToken\s*=\s*\'(\w+)\''
        ajax_token_compile = re.compile(pattern)
        ajax_token = ajax_token_compile.findall(html)[0]
        return ajax_token

    def get_nation(self):
        html = self.login.login()
        nation_compile = re.compile('nation(\d)')
        nation = nation_compile.findall(html)[0]
        return NATIONS[int(nation)]

    def get_village_ids(self):
        html = self.login.login()
        pattern = r'<a  href="\?newdid=(\d+)&amp;"'
        village_village_ids_compile = re.compile(pattern)
        village_village_ids = village_village_ids_compile.findall(html)
        return village_village_ids

    def get_village_amount(self):
        village_vids = self.get_village_ids()
        village_amount = len(village_vids)
        return village_amount

    def get_village_names(self):
        html = self.login.login()
        #pattern = r'<li class="[.\s\d]{0,}" title="(.*)\s&lrm;&amp;#x202d;'
        pattern = r'<div class="name">(.*)</div>'
        regex = re.compile(pattern)
        names = regex.findall(html)
        return names

    def get_village_pos(self):
        html = self.login.login()
        pattern = r'coordinateX">\(&#x202d;&(#45;)*&*#x202d;(\d+)'
        x_compile = re.compile(pattern)
        X = x_compile.findall(html)
        pattern = r'coordinateY">&#x202d;&(#45;)*&*#x202d;(\d+)'
        y_compile = re.compile(pattern)
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
        return pos

    def get_warehouse(self):
        html = self.login.login()
        pattern = r'<span class="value" id="stockBarWarehouse">(\d*)</span>'
        warehouse = int(re.findall(pattern, html)[0])
        return warehouse

    def get_granary(self):
        html = self.login.login()
        pattern = r'<span class="value" id="stockBarGranary">(\d*)</span>'
        granary = int(re.findall(pattern, html)[0])
        return granary

    def get_resources(self):
        html = self.login.login()
        pattern = r'<span id="l\d" class="value">(\d*)</span>'
        raw_resources = re.findall(pattern, html)
        resources = [int(p) for p in raw_resources]
        return resources

    def get_production(self):
        html = self.login.login()
        pattern = r'‎&#x202d;&#x202d;(\d*)&#x202c;&#x202c;'
        raw_production = re.findall(pattern, html)
        production = [int(p) for p in raw_production]
        return production
