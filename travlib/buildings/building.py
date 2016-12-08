import re
import bs4


class Building:
    """
    Class Building is base class for all buildings in the API.
    """
    def __init__(self, village_part, name: str, id: int, level: int):
        self.village_part = village_part
        self.name = name
        self.id = id
        self._level = level
        self.eng_name = ''

    def get_level(self):
        html = self.village_part.get_html({'id': self.id})
        soup = bs4.BeautifulSoup(html, 'html5lib')
        span_level = soup.find('span', {'class': 'level'})
        level = int(re.findall(r' (\d+)', span_level.text)[0])
        self._level = level
        return level
    level = property(get_level)

    def get_build_index(self):
        html = self.village_part.get_html({'id': self.id})
        soup = bs4.BeautifulSoup(html, 'html5lib')
        div_building_wraper = soup.find('div', {'class': 'buildingWrapper'})
        if not div_building_wraper:
            a_build_logo = soup.find('a', {'class': 'build_logo'})
            img_big_white = a_build_logo.find('img')
            building_name = img_big_white['alt']
            building_index = int(img_big_white['class'][2][1:])
            return building_name, building_index
        else:
            # Стройплощадка
            return 0

    def build(self):
        html = self.village_part.get_html({'id': self.id})
        try:
            result = re.search(r'(?<=&amp;c=)(\w+)', html)
        # maybe not enough resource.
        except:
            return False
        if result is None:
            return False
        print('Start Building on Village ' + str(self.village_part.id) + ' field ' + str(self.id))
        c = result.group(0)
        self.village_part.start_build(self.id, c)
