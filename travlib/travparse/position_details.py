import bs4


def _parse_abandoned_valley(div_content_container: bs4.NavigableString):
    info = dict()
    info['type'] = 'abandoned-valley'
    # get distribution
    table_distribution = div_content_container.find('table', {'id': 'distribution'})
    td_val_all = table_distribution.find_all('td', {'class': 'val'})
    distribution = [int(td.text.strip()) for td in td_val_all]
    info['distribution'] = tuple(distribution)
    return info


def _parse_village(div_content_container: bs4.NavigableString):
    if not div_content_container.find('table', {'id': 'village_info'}):
        return _parse_abandoned_valley(div_content_container)
    info = dict()
    info['type'] = 'village'
    # get distribution
    table_distribution = div_content_container.find('table', {'id': 'distribution'})
    td_all = table_distribution.find_all('td')
    distribution = [int(td.text.strip()) for td in td_all]
    info['distribution'] = tuple(distribution)
    # get nation
    table_village_info = div_content_container.find('table', {'id': 'village_info'})
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


def _parse_oasis(div_content_container: bs4.NavigableString):
    info = dict()
    info['type'] = 'oasis'
    # get distribution
    table_distribution = div_content_container.find('table', {'id': 'distribution'})
    tr_all = table_distribution.find_all('tr')
    distribution = []
    for tr in tr_all:
        td_ico = tr.find('td', {'class': 'ico'})
        img = td_ico.find('img')
        resource_type = int(img['class'][0][-1])
        td_val = tr.find('td', {'class': 'val'})
        value = float(
            td_val.text.replace('\u200e', '').replace('\u202d', '').replace('\u202c', '').strip('\n\t %')) / 100
        distribution.append((resource_type, value))
    info['distribution'] = tuple(distribution)
    return info


def _parse_landscape(div_content_container: bs4.NavigableString):
    info = dict()
    info['type'] = 'landscape'
    return info


def get_pos_info(soup: bs4.BeautifulSoup) -> dict:
    # div_contentTitle = soup.find('div', {'class': 'contentTitle'})
    div_content_container = soup.find('div', {'class': 'contentContainer'})
    point_type = div_content_container.find('div', {'id': 'tileDetails'})['class'][0]
    info = dict()
    info['distribution'] = (0, 0, 0, 0)
    info['nation'] = ''
    info['alliance'] = ''
    info['player'] = ''
    info['population'] = 0
    if point_type == 'village':
        info.update(_parse_village(div_content_container))
    elif point_type == 'oasis':
        info.update(_parse_oasis(div_content_container))
    elif point_type == 'landscape':
        info.update(_parse_landscape(div_content_container))
    return info
