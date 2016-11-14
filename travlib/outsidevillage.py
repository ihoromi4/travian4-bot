import re

class OutsideVillage:
    def __init__(self, village):
        self.village = village
        self.login = village.login
        self.id = village.id

    def get_buildings(self):
        html_text = self.login.load_dorf1(self.id).text
        pattern = r'alt="(\b.*\b) Уровень (\d*)"/><area href='
        buildings = re.findall(pattern, html_text)
        return buildings
