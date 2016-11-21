import re

import bs4

from . import buildings
from .buildings import marketplace


class InsideVillage:
    def __init__(self, village):
        self.village = village
        self.login = village.login
        self.id = village.id
        self.buildings = []
        # ---
        self.marketplace = None
        self.create_buildings()

    def get_html(self, params={}):
        return self.village.get_html("build.php", params=params)

    def start_build(self, building_id, c):
        self.village.get_html('dorf2.php', {'a': building_id, 'c': c})

    def create_buildings(self):
        buildings_list = self.get_buildings()
        for building_info in buildings_list:
            name = building_info['name']
            id = building_info['id']
            level = building_info['level']
            repr = self.village.account.langdata.data["buildings"].get(name, "")
            building_type = buildings.get_building_type(repr)
            building = building_type(self, name, id, level)
            if building_type is marketplace.Marketplace:
                self.marketplace = building
            self.buildings.append(building)

    def get_buildings(self):
        html = self.login.load_dorf2(self.id)
        soup = bs4.BeautifulSoup(html, 'html5lib')
        building_list = soup.find_all('area')
        buildings = []
        for building in building_list:
            building_dict = dict()
            alt = building['alt']
            if re.fullmatch(r'\S*', alt):
                name = alt
                level = 0
                id = re.findall(r'id=(\d+)', building['href'])[0]
            else:
                name, level = re.findall(r'(\b.+\b) <span class="level">\b\S+\b (\d+)</span>', alt)[0]
                id = re.findall(r'id=(\d+)', building['href'])[0]
            building_dict['name'] = name
            building_dict['level'] = level
            building_dict['id'] = id
            buildings.append(building_dict)
        return buildings
