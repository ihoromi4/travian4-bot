import re

import bs4

from . import buildings
from .buildings import resourcefield


class OutsideVillage:
    def __init__(self, village):
        self.village = village
        self.login = village.login
        self.id = village.id
        self.resource_fields = []
        self.create_resource_fields()

    def get_html(self, params={}):
        return self.village.get_html("build.php", params=params)

    def start_build(self, building_id, c):
        self.village.get_html('dorf1.php', {'a': building_id, 'c': c})

    def create_resource_fields(self):
        resource_fields = self.get_resource_fields()
        for field_info in resource_fields:
            name = field_info['name']
            id = field_info['id']
            level = field_info['level']
            building_type = buildings.get_building_type(name)
            field = building_type(self, name, id, level)
            self.resource_fields.append(field)

    def get_resource_fields(self):
        html = self.login.load_dorf1(self.id)
        # pattern = r'alt="(\b.*\b) Уровень (\d*)"/><area href='
        # buildings = re.findall(pattern, html_text)
        soup = bs4.BeautifulSoup(html, 'html5lib')
        fields_data = soup.find_all('area')[:-1]
        resource_fields = []
        for field in fields_data:
            field_dict = dict()
            field_dict['name'], field_dict['level'] = re.findall(r'(.+) \b\S+\b (\d+)', field['alt'])[0]
            field_dict['id'] = re.findall(r'id=(\d+)', field['href'])[0]
            resource_fields.append(field_dict)
        return resource_fields
