import re

import bs4

from . import buildings
from .buildings import resourcefield


class OutsideVillage:
    def __init__(self, village):
        self.village = village
        self.login = village.login
        self.id = village.id
        self.buildings = []
        self.create_resource_fields()

    def get_html(self, params={}):
        return self.village.get_html("build.php", params=params)

    def get_building_by_id(self, id: int):
        for build in self.buildings:
            if build.id == id:
                return build
        return None

    def start_build(self, building_id, c):
        self.village.get_html('dorf1.php', {'a': building_id, 'c': c})

    def create_resource_fields(self):
        resource_fields = self.read_resource_fields()
        for field_info in resource_fields:
            name = field_info['name']
            id = field_info['id']
            level = field_info['level']
            repr = self.village.account.langdata.data["buildings"].get(name, "")
            building_type = buildings.get_building_type(repr)
            field = building_type(self, name, id, level)
            self.buildings.append(field)

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
            field_dict['id'] = int(re.findall(r'id=(\d+)', field['href'])[0])
            resource_fields.append(field_dict)
        return resource_fields

    def read_resource_fields(self):
        html = self.login.load_dorf1(self.id)
        soup = bs4.BeautifulSoup(html, 'html5lib')
        village_map = soup.find('map', {'name': 'rx'})
        areas = village_map.find_all('area')
        resource_fields = []
        for area in areas:
            resource_field = {}
            href = area['href']
            id_list = re.findall(r'id=(\d+)', href)
            if not id_list:
                continue
            id = int(id_list[0])
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
            resource_field['name'] = name
            resource_field['level'] = level
            resource_field['id'] = id
            resource_field['is_build'] = is_build
            resource_field['is_top_level'] = is_top_level
            resource_field['resources_to_build'] = resources_to_build
            resource_fields.append(resource_field)
        return resource_fields
