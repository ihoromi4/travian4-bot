import json
import re

import bs4

from . import building


class Marketplace(building.Building):
    def __init__(self, village_part, name, id, level):
        building.Building.__init__(self, village_part, name, id, level)
        self.eng_name = 'marketplace'
        self._max_merchants = 0
        self._free_merchants = 0
        self._busy_on_marketplace_merchants = 0
        self._merchants_in_travel = 0

    def get_data(self):
        html = self.village_part.get_html({'id': self.id, 't': 0})
        soup = bs4.BeautifulSoup(html, 'html5lib')
        merchants = soup.find_all('div', {'class': 'whereAreMyMerchants'})[0]
        text = merchants.text
        merchants_data = re.findall(r'(\d+)', text)
        self._free_merchants = int(merchants_data[0])
        self._max_merchants = int(merchants_data[1])
        self._busy_on_marketplace_merchants = int(merchants_data[3])
        self._merchants_in_travel = int(merchants_data[4])

    def get_max_merchants(self) -> int:
        self.get_data()
        return self._max_merchants
    max_merchants = property(get_max_merchants)

    def get_free_merchants(self) -> int:
        self.get_data()
        return self._free_merchants
    free_merchants = property(get_free_merchants)

    def get_busy_on_marketplace_merchants(self) -> int:
        self.get_data()
        return self._busy_on_marketplace_merchants
    busy_on_marketplace_merchants = property(get_busy_on_marketplace_merchants)

    def get_merchants_in_travel(self) -> int:
        self.get_data()
        return self._merchants_in_travel
    merchants_in_travel = property(get_merchants_in_travel)

    def get_page_amount(self) -> int:
        html = self.village_part.get_html({'id': self.id, 't': 1})
        soup = bs4.BeautifulSoup(html, 'html5lib')
        paginator = soup.find('div', {'class': 'paginator'})
        contents = paginator.children
        page_amount = 1
        for element in contents:
            try:
                page_amount = max(page_amount, int(element.string))
            except TypeError:
                pass
            except ValueError:
                pass
        return page_amount

    def get_page(self, page=1) -> list:
        html = self.village_part.get_html({'id': self.id, 't': 1, 'page': page})
        soup = bs4.BeautifulSoup(html, 'html5lib')
        table = soup.find('table', {'id': "range"})
        rows = table.find_all('tr')[1:]
        biddings = []
        for row in rows:
            bid = {}
            elements = row.find_all('td')
            f1 = int(elements[0].text.strip())
            f1_type_name = elements[0].find('img')['alt']
            f1_type = self.village_part.login.language.resource_to_int(f1_type_name)
            bid['offering'] = (f1, f1_type)
            relation = float(elements[1].text.strip())
            bid['relation'] = relation
            f2 = int(elements[2].text.strip())
            f2_type_name = elements[2].find('img')['alt']
            f2_type = self.village_part.login.language.resource_to_int(f2_type_name)
            bid['searching'] = (f2, f2_type)
            player = elements[3].find('a').text
            bid['player'] = player
            time = elements[4].text.strip()
            bid['time'] = time
            #print(elements[5]['class'])
            biddings.append(bid)
        return biddings

    def get_pages(self, max_page=99) -> list:
        biddings = []
        max_page = min(max_page, self.get_page_amount())
        for page in range(1, max_page + 1):
            biddings.extend(self.get_page(page))
        return biddings

    def send_resources(self, name_or_pos, res=[0, 0, 0, 0]) -> bool:
        login = self.village_part.village.login
        ajax_token = self.village_part.village.account.ajax_token
        html = self.village_part.get_html({'id': self.id, 't': '5'})
        data = dict()
        for i in range(0, 4):
            data["r{}".format(i+1)] = str(res[i])
        data['dname'] = ''
        data['x'] = ''
        data['y'] = ''
        if type(name_or_pos) is str:
            data['dname'] = name_or_pos
        elif type(name_or_pos) in (tuple, list):
            if len(name_or_pos) == 2:
                data['x'] = str(name_or_pos[0])
                data['y'] = str(name_or_pos[1])
        else:
            raise TypeError("name_or_pos wrong argument type")
        data['id'] = str(self.id)
        data['t'] = '5'
        data['x2'] = '1'
        data['ajaxToken'] = ajax_token
        data['cmd'] = 'prepareMarketplace'
        html = login.get_ajax('ajax.php', data=data)
        response = json.loads(html)['response']
        if response['error']:
            print('send resource: error true')
            return False
        print(response['data'])
        with open('mpt5.html', 'w') as stream:
            stream.write(html)
        bs = bs4.BeautifulSoup(html, 'html5lib')
        form = bs.find('form')
        if not form:
            return False
        for i in form.children:
            if i.name == 'input':
                data[i['name'].strip('\\\"\'')] = i['value'].strip('\\\"\'')
        html = login.get_ajax('ajax.php', data=data)
        return True
