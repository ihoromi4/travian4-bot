import re
import bs4

from . import building


class Marketplace(building.Building):
    def __init__(self, village_part, name, id, level):
        building.Building.__init__(self, village_part, name, id, level)
        self.eng_name = 'marketplace'

    def get_data(self):
        html = self.village_part.get_html({'id': self.id, 't': 0})
        soup = bs4.BeautifulSoup(html, 'html5lib')
        merchants = soup.find_all('div', {'class': 'whereAreMyMerchants'})[0]
        text = merchants.text
        merchants_data = re.findall(r'(\d+)', text)
        free_merchants = merchants_data[0]
        max_merchants = merchants_data[1]
        busy_on_marketplace_merchants = merchants_data[3]
        merchants_in_travel = merchants_data[4]
        print(max_merchants)
        print(free_merchants)
        print(busy_on_marketplace_merchants)
        print(merchants_in_travel)

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
