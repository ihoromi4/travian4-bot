import logging
import re

import bs4

from .buildings import marketplace
from .buildings import palace
from .buildings import residence

from . import buildings
from .buildings import townhall


class InnerVillage:
    def __init__(self, village):
        self.village = village
        self.login = village.login
        self.id = village.id
        self.__buildings = {}
        # ---
        self.__create_buildings()

    def get_html(self, params={}):      # obs
        return self.village.get_html("build.php", params=params)

    def get_building_html(self, params={}):
        return self.village.get_html("build.php", params=params)

    def get_buildings(self):
        self._update_buildings()
        return list(self.__buildings.values())
    buildings = property(get_buildings)

    def get_building(self, inner_repr: str):
        for building in self.buildings:
            if building.inner_repr == inner_repr:
                return building
        return None

    def get_building_by_id(self, id: int):
        for build in self.buildings:
            if build.id == id:
                return build
        return None

    def start_build(self, building_id: int, c: int):
        self.village.get_html('dorf2.php', {'a': building_id, 'c': c})

    def __create_buildings(self):
        buildings_list = self._parse_dorf2_village_map()
        for building_info in buildings_list:
            name = building_info['name']
            id = building_info['id']
            level = building_info['level']
            # repr = self.village.account.language.data["buildings"].get(name, "")
            repr = building_info['repr']
            building_type = buildings.get_building_type(repr)
            building = building_type(self, name, id, level)
            building.inner_repr = repr
            self.__buildings[id] = building

    def _update_buildings(self):
        buildings_list = self._parse_dorf2_village_map()
        for info in buildings_list:
            building = self.__buildings[info['id']]
            if building.inner_repr == info['repr']:
                building.level = info['level']
                building.is_build = info['is_build']
                building.is_top_level = info['is_top_level']
                building.cost_for_upgrading = info['resources_to_build']
            else:
                name = info['name']
                id = info['id']
                level = info['level']
                repr = info['repr']
                logging.debug('Change building type from {} to {}'.format(building.inner_repr, repr))
                building_type = buildings.get_building_type(repr)
                building = building_type(self, name, id, level)
                building.inner_repr = repr
                self.__buildings[id] = building

    def __get_buildings_index_types(self, village_map):
        images = village_map.find_all('img')
        building_types = {}
        for img in images:
            if img['class'][0] in ('building', 'wall'):
                alt = img['alt']
                if 'span' in alt:
                    name = re.findall(r'(.+) <span', img['alt'])[0]
                    index = int(re.findall(r'g(\d+)', img['class'][1])[0])
                else:
                    name = alt
                    index = 0
                try:
                    building_repr = self.village.account.language.index_to_building_repr(index)
                except KeyError:
                    print(name, index)
                    raise
                self.village.account.language.set_repr_to_local_language(building_repr, name)
                building_types[name] = building_repr
        return building_types

    def _parse_dorf2_village_map(self):
        html = self.login.load_dorf2(self.id)
        soup = bs4.BeautifulSoup(html, 'html5lib')
        village_map = soup.find('div', {'id': 'village_map'})
        # ---
        building_types = self.__get_buildings_index_types(village_map)
        # ---
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
            building['repr'] = building_types[name]
            building['is_build'] = is_build
            building['is_top_level'] = is_top_level
            building['resources_to_build'] = resources_to_build
            buildings.append(building)
        return buildings

    def downgrade(self, building):
        name = building.name
        id = building.id
        print('Downgrade building {}, id = {}'.format(name, id))
