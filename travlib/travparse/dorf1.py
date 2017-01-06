import bs4

import re


def parse_ajax_token(html: str) -> str:
    pattern = r'ajaxToken\s*=\s*\'(\w+)\''
    ajax_token_compile = re.compile(pattern)
    results = ajax_token_compile.findall(html)
    if len(results):
        ajax_token = results[0]
        return ajax_token
    raise TypeError('Page sources not contain ajax token')


def parse_server_time(soup: bs4.BeautifulSoup) -> str:
    div_server_time = soup.find('div', {'id': 'servertime'})
    span_timer = div_server_time.find('span', {'class': 'timer'})
    server_time = span_timer.text
    return server_time


def parse_nation_id(soup: bs4.BeautifulSoup) -> int:
    div_player_name = soup.find('div', {'class': 'playerName'})
    img = div_player_name.find('img')
    nation_id = int(img['class'][1][-1])
    return nation_id


def parse_gold(soup: bs4.BeautifulSoup) -> int:
    gold_silver_container = soup.find('div', {'id': 'goldSilverContainer'})
    gold_container = gold_silver_container.find('div', {'class': 'gold'})
    gold_span = gold_container.find('span', {'class': 'ajaxReplaceableGoldAmount'})
    return int(gold_span.text)


def parse_silver(soup: bs4.BeautifulSoup) -> int:
    gold_silver_container = soup.find('div', {'id': 'goldSilverContainer'})
    silver_container = gold_silver_container.find('div', {'class': 'silver'})
    silver_span = silver_container.find('span', {'class': 'ajaxReplaceableSilverAmount'})
    return int(silver_span.text)


def parse_villages_data(soup: bs4.BeautifulSoup) -> list:
    div = soup.find('div', {'id': 'sidebarBoxVillagelist'})
    inner_box = div.find('div', {'class': 'innerBox content'})
    all_li = inner_box.find_all('li')
    villages_data = []
    for li in all_li:
        village = {}
        href = li.find('a')['href']
        id = int(re.findall(r'id=(\d+)&', href)[0])
        village['id'] = id

        div_name = li.find('div', {'class': 'name'})
        name = div_name.text
        village['name'] = name

        strip = lambda x: x.replace('\u202d', '').replace('\u202c', '').strip('()')
        span_x = li.find('span', {'class': 'coordinateX'})
        x = int(strip(span_x.text))
        span_y = li.find('span', {'class': 'coordinateY'})
        y = int(strip(span_y.text))
        village['coords'] = (x, y)
        villages_data.append(village)
    return villages_data
