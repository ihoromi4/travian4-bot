import re
import bs4


class Building:
    """
    Class Building is base class for all buildings in the API.
    """
    def __init__(self, village_part, name, id, level):
        self.village_part = village_part
        self.name = name
        self.id = id
        self.level = level
        self.eng_name = ''

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
