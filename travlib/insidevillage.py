import re
import bs4

from . import building


class InsideVillage:
    def __init__(self, village):
        self.village = village
        self.login = village.login
        self.id = village.id
        self.buildings = []
        self.create_buildings()

    def create_buildings(self):
        buildings = self.get_buildings()
        for building_info in buildings:
            building_ = building.Building(self, building_info['name'], building_info['id'], building_info['level'])
            self.buildings.append(building_)

    def get_buildings(self):
        html = self.login.load_dorf2(self.id).text
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
                name, level = re.findall(r'(.+) <span class="level">.+ (\d+)</span>', alt)[0]
                id = re.findall(r'id=(\d+)', building['href'])[0]
            building_dict['name'] = name
            building_dict['level'] = level
            building_dict['id'] = id
            buildings.append(building_dict)
        return buildings
