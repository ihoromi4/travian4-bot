import re
import bs4

from . import outsidevillage
from . import insidevillage


class Village:
    def __init__(self, account, id, pos):
        self.account = account
        self.login = account.login
        self.id = id
        self.pos = tuple(pos)
        # ---
        self.outside = outsidevillage.OutsideVillage(self)
        self.inside = insidevillage.InsideVillage(self)

    def get_html(self, last_url='', params={}):
        params['newdid'] = self.id
        return self.login.get_html(last_url, params=params)

    def get_name(self) -> str:
        html_text = self.login.load_dorf1(self.id)
        pattern = r'<div id="villageNameField" class="boxTitle">(.*)</div>'
        regex = re.compile(pattern)
        names = regex.findall(html_text)
        return names[0]
    name = property(get_name)

    def get_warehouse(self) -> float:
        html_text = self.login.load_dorf1(self.id)
        pattern = r'<span class="value" id="stockBarWarehouse">(\d*)</span>'
        warehouse = int(re.findall(pattern, html_text)[0])
        return warehouse
    warehouse = property(get_warehouse)

    def get_granary(self) -> float:
        html_text = self.login.load_dorf1(self.id)
        pattern = r'<span class="value" id="stockBarGranary">(\d*)</span>'
        granary = int(re.findall(pattern, html_text)[0])
        return granary
    granary = property(get_granary)

    def get_resources(self) -> list:
        html_text = self.login.load_dorf1(self.id)
        pattern = r'<span id="l\d" class="value">(\d*)</span>'
        raw_resources = re.findall(pattern, html_text)
        resources = [int(p) for p in raw_resources]
        return resources
    resources = property(get_resources)

    def get_production(self) -> list:
        html_text = self.login.load_dorf1(self.id)
        pattern = r'‎&#x202d;&#x202d;(\d*)&#x202c;&#x202c;'
        raw_production = re.findall(pattern, html_text)
        production = [int(p) for p in raw_production]
        return production
    production = property(get_production)

    def get_free_crop(self):
        html = self.login.load_dorf1(self.id)
        soup = bs4.BeautifulSoup(html, 'html5lib')
        span_free_crop = soup.find('span', {'id': 'stockBarFreeCrop'})
        free_crop = int(span_free_crop.text)
        return free_crop
    free_crop = property(get_free_crop)

    def get_builds(self) -> list:
        builds = []
        resource_fields_list = self.outside.read_resource_fields()
        for rf in resource_fields_list:
            if rf['is_build']:
                building = self.outside.get_building_by_id(rf['id'])
                builds.append(building)
        building_list = self.inside.read_buildings()
        for b in building_list:
            if b['is_build']:
                building = self.inside.get_building_by_id(b['id'])
                builds.append(building)
        return builds
    builds = property(get_builds)

    def read_builds(self):
        html = self.login.load_dorf1(self.id)
        soup = bs4.BeautifulSoup(html, 'html5lib')
        building_list = soup.find('div', {'class': 'boxes buildingList'})
        ul = building_list.find('ul')
        all_li = ul.find_all('li')
        builds = []
        for li in all_li:
            build = {}
            div_name = li.find('div', {'class': 'name'})
            name = div_name.contents[0].strip()
            span_level = li.find('span', {'class': 'lvl'})
            level = int(re.findall(r' (\d+)', span_level.text)[0])
            div_duration = li.find('div', {'class': 'buildDuration'})
            duration = re.findall(r'(\d+:\d\d:\d\d)', div_duration.text)[0]
            time = re.findall(r' (\d+:\d\d)', div_duration.text)[0]
            print(name, level, duration, time)
            build['name'] = name
            build['level'] = level
            build['duration'] = duration
            build['time'] = time
            builds.append(build)
        return builds

    def get_building_by_id(self, id: int):
        return self.inside.get_building_by_id(id) or \
                self.outside.get_building_by_id(id)
