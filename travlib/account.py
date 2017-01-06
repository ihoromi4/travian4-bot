import bs4

from .travparse import dorf1
from .travparse import spieler

from . import login
from .event import eventmachine
from .village import village
from . import reports
from . import map

NATIONS = ['romans', 'teutons', 'gauls']

RESOURCE_TYPES = ['lumber', 'clay', 'iron', 'crop']
LUMBER = 0
CLAY = 1
IRON = 2
CROP = 3


class Account(eventmachine.EventMachine):
    def __init__(self, url, name, password, headers={}):
        self.login = login.Login(url, name, password, headers)
        self.language = self.login.language
        self.__villages = {}  # id: village
        self.nation = NATIONS[self.nation_id-1]
        self.map = map.Map(self)
        self.reports = reports.Reports(self)

    def get_server_time(self):
        html = self.login.get_html("dorf1.php")
        soup = bs4.BeautifulSoup(html, 'html5lib')
        return dorf1.parse_server_time(soup)
    server_time = property(get_server_time)

    def get_rank(self) -> int:
        html = self.login.get_html("spieler.php")
        soup = bs4.BeautifulSoup(html, 'html5lib')
        return spieler.parse_rank(soup)
    rank = property(get_rank)

    def get_alliance(self) -> int:
        html = self.login.get_html("spieler.php")
        soup = bs4.BeautifulSoup(html, 'html5lib')
        return spieler.parse_alliance(soup)
    alliance = property(get_alliance)

    def get_villages_amount(self) -> int:
        html = self.login.get_html("spieler.php")
        soup = bs4.BeautifulSoup(html, 'html5lib')
        return spieler.parse_villages_amount(soup)
    villages_amount = property(get_villages_amount)

    def get_population(self):
        html = self.login.get_html("spieler.php")
        soup = bs4.BeautifulSoup(html, 'html5lib')
        return spieler.parse_population(soup)
    population = property(get_population)

    def get_nation_id(self):
        html = self.login.get_html("dorf1.php")
        soup = bs4.BeautifulSoup(html, 'html5lib')
        return dorf1.parse_nation_id(soup)
    nation_id = property(get_nation_id)

    def update_villages(self):
        villages_data = self._load_villages_data()
        for vdata in villages_data:
            id = vdata['id']
            pos = vdata['coords']
            if id not in self.__villages:
                vil = village.Village(self, id, pos)
                self.__villages[id] = vil

    def get_villages(self) -> village.Village:
        self.update_villages()
        return list(self.__villages.values())
    villages = property(get_villages)

    def get_villages_names(self) -> list:
        names = [self.__villages[id].name for id in self.__villages]
        return names
    villages_names = property(get_villages_names)

    def get_ajax_token(self):
        html = self.login.get_html("dorf1.php")
        return dorf1.parse_ajax_token(html)
    ajax_token = property(get_ajax_token)

    def _load_villages_data(self):
        html = self.login.get_html("dorf1.php")
        soup = bs4.BeautifulSoup(html, 'html5lib')
        return dorf1.parse_villages_data(soup)

    def read_spieler(self):
        html = self.login.get_html("spieler.php")
        soup = bs4.BeautifulSoup(html, 'html5lib')
        return spieler.parse_spieler(soup)

    def get_village_by_id(self, id: int):
        self.update_villages()
        return self.__villages[id]

    def get_village_by_name(self, name: str):
        for village in self.villages:
            if village.name == name:
                return village
        return None

    def get_gold(self):
        html = self.login.get_html("dorf1.php")
        soup = bs4.BeautifulSoup(html, 'html5lib')
        return dorf1.parse_gold_silver(soup)['gold']
    gold = property(get_gold)

    def get_silver(self):
        html = self.login.get_html("dorf1.php")
        soup = bs4.BeautifulSoup(html, 'html5lib')
        return dorf1.parse_gold_silver(soup)['silver']
    silver = property(get_silver)