import re

import bs4

from . import buildings
from .buildings import marketplace
from .buildings import residence
from .buildings import palace
from .buildings import townhall


class InsideVillage:
    def __init__(self, village):
        self.village = village
        self.login = village.login
        self.id = village.id
        self.buildings = []
        # ---
        self.main_building = None
        self.marketplace = None
        self.residence = None
        self.palace = None
        self.townhall = None
        self.create_buildings()

    def get_html(self, params={}):
        return self.village.get_html("build.php", params=params)

    def get_building_by_id(self, id: int):
        for build in self.buildings:
            if build.id == id:
                return build
        return None

    def start_build(self, building_id, c):
        self.village.get_html('dorf2.php', {'a': building_id, 'c': c})

    def create_buildings(self):
        buildings_list = self.read_buildings()
        for building_info in buildings_list:
            name = building_info['name']
            id = building_info['id']
            level = building_info['level']
            repr = self.village.account.langdata.data["buildings"].get(name, "")
            building_type = buildings.get_building_type(repr)
            building = building_type(self, name, id, level)
            if building_type is marketplace.Marketplace:
                self.marketplace = building
            elif building_type is residence.Residence:
                self.residence = building
            elif building_type is palace.Palace:
                self.palace = building
            elif building_type is townhall.TownHall:
                self.townhall = building
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
                id = int(re.findall(r'id=(\d+)', building['href'])[0])
            building_dict['name'] = name
            building_dict['level'] = level
            building_dict['id'] = id
            buildings.append(building_dict)
        return buildings

    def read_buildings(self):
        html = self.login.load_dorf2(self.id)
        soup = bs4.BeautifulSoup(html, 'html5lib')
        village_map = soup.find('div', {'id': 'village_map'})
        areas = village_map.find_all('area')
        buildings = []
        for area in areas:
            building = {}
            href = area['href']
            id = int(re.findall(r'id=(\d+)', href)[0])
            title = area['title']
            if title.find('span') == -1:
                name = title
                level = 0
                resources_to_build = None
                is_build = False
                is_top_level = False
            else:
                s = bs4.BeautifulSoup(title, 'html5lib')
                body = s.find('body')
                name = str(body.contents[0]).strip()
                level_text = body.find('span', {'class': 'level'}).text
                level = int(re.findall(r' (\d+)', level_text)[0])
                build_notice = body.find('span', {'class': 'notice'})
                is_build = bool(build_notice)
                resources_to_build = []
                for r in body.find_all('span', {'class': 'resources'}):
                    resources_to_build.append(int(r.contents[2]))
                is_top_level = not bool(resources_to_build)
            building['name'] = name
            building['level'] = level
            building['id'] = id
            building['is_build'] = is_build
            building['is_top_level'] = is_top_level
            building['resources_to_build'] = resources_to_build
            buildings.append(building)
        return buildings
