import bs4


class Map:
    def __init__(self, account):
        self.account = account

    def _parse_abandoned_valley(self, div_contentContainer):
        info = dict()
        info['type'] = 'abandoned-valley'
        # get distribution
        table_distribution = div_contentContainer.find('table', {'id': 'distribution'})
        td_val_all = table_distribution.find_all('td', {'class': 'val'})
        distribution = [int(td.text.strip()) for td in td_val_all]
        info['distribution'] = tuple(distribution)
        return info

    def _parse_village(self, div_contentContainer):
        if not div_contentContainer.find('table', {'id': 'village_info'}):
            return self._parse_abandoned_valley(div_contentContainer)
        info = dict()
        info['type'] = 'village'
        # get distribution
        table_distribution = div_contentContainer.find('table', {'id': 'distribution'})
        td_all = table_distribution.find_all('td')
        distribution = [int(td.text.strip()) for td in td_all]
        info['distribution'] = tuple(distribution)
        # get nation
        table_village_info = div_contentContainer.find('table', {'id': 'village_info'})
        all_td = table_village_info.find_all('td')
        nation = all_td[0].text.strip().lower()
        info['nation'] = nation
        # get aliance
        alliance = all_td[1].text.strip()
        info['alliance'] = alliance
        # get player
        player = all_td[2].text.strip()
        info['player'] = player
        # get population
        population = int(all_td[3].text.strip())
        info['population'] = population
        return info

    def _parse_oasis(self, div_contentContainer):
        info = dict()
        info['type'] = 'oasis'
        # get distribution
        table_distribution = div_contentContainer.find('table', {'id': 'distribution'})
        tr_all = table_distribution.find_all('tr')
        distribution = []
        for tr in tr_all:
            td_ico = tr.find('td', {'class': 'ico'})
            img = td_ico.find('img')
            resource_type = int(img['class'][0][-1])
            td_val = tr.find('td', {'class': 'val'})
            value = float(td_val.text.replace('\u200e', '').replace('\u202d', '').replace('\u202c', '').strip('\n\t %')) / 100
            distribution.append((resource_type, value))
        info['distribution'] = tuple(distribution)
        return info

    def _parse_landscape(self, div_contentContainer):
        info = dict()
        info['type'] = 'landscape'
        return info

    def get_pos_info(self, pos):
        params = {'x': pos[0], 'y': pos[1]}
        html = self.account.login.server_get('position_details.php', params=params)
        soup = bs4.BeautifulSoup(html, 'html5lib')
        div_contentTitle = soup.find('div', {'class': 'contentTitle'})
        div_contentContainer = soup.find('div', {'class': 'contentContainer'})
        point_type = div_contentContainer.find('div', {'id': 'tileDetails'})['class'][0]
        info = dict()
        info['distribution'] = (0, 0, 0, 0)
        info['nation'] = ''
        info['alliance'] = ''
        info['player'] = ''
        info['population'] = 0
        info['pos'] = pos
        if point_type == 'village':
            info.update(self._parse_village(div_contentContainer))
        elif point_type == 'oasis':
            info.update(self._parse_oasis(div_contentContainer))
        elif point_type == 'landscape':
            info.update(self._parse_landscape(div_contentContainer))
        return info
