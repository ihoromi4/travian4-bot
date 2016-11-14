import re

from . import outsidevillage
from . import insidevillage

class Village:
    def __init__(self, account, id):
        self.account = account
        self.login = account.login
        self.id = id
        # ---
        self.outside = outsidevillage.OutsideVillage(self)
        self.inside = insidevillage.InsideVillage(self)

    def get_name(self) -> str:
        html_text = self.login.load_dorf1(self.id).text
        pattern = r'<div id="villageNameField" class="boxTitle">(.*)</div>'
        regex = re.compile(pattern)
        names = regex.findall(html_text)
        return names[0]
    name = property(get_name)

    def get_warehouse(self) -> float:
        html_text = self.login.load_dorf1(self.id).text
        pattern = r'<span class="value" id="stockBarWarehouse">(\d*)</span>'
        warehouse = int(re.findall(pattern, html_text)[0])
        return warehouse
    warehouse = property(get_warehouse)

    def get_granary(self) -> float:
        html_text = self.login.load_dorf1(self.id).text
        pattern = r'<span class="value" id="stockBarGranary">(\d*)</span>'
        granary = int(re.findall(pattern, html_text)[0])
        return granary
    granary = property(get_granary)

    def get_resources(self) -> list:
        html_text = self.login.load_dorf1(self.id).text
        pattern = r'<span id="l\d" class="value">(\d*)</span>'
        raw_resources = re.findall(pattern, html_text)
        resources = [int(p) for p in raw_resources]
        return resources
    resources = property(get_resources)

    def get_production(self) -> list:
        html_text = self.login.load_dorf1(self.id).text
        pattern = r'‎&#x202d;&#x202d;(\d*)&#x202c;&#x202c;'
        raw_production = re.findall(pattern, html_text)
        production = [int(p) for p in raw_production]
        return production
    production = property(get_production)

    def get_builds(self) -> list:
        html_text = self.login.load_dorf1(self.id).text
        pattern = r'<div class="name">\s*\b(.*)\b\s*<span class="lvl">Уровень (\d*)</span>\s*</div>'
        builds = re.findall(pattern, html_text)
        return builds
