import re
import bs4


def parse_t0(soup: bs4.BeautifulSoup) -> dict:
    merchants = soup.find_all('div', {'class': 'whereAreMyMerchants'})[0]
    text = merchants.text
    merchants_data = re.findall(r'(\d+)', text)
    data = dict()
    data['free_merchants'] = int(merchants_data[0])
    data['max_merchants'] = int(merchants_data[1])
    data['busy_on_marketplace_merchants'] = int(merchants_data[3])
    data['merchants_in_travel'] = int(merchants_data[4])
    return data


def parse_t1(soup: bs4.BeautifulSoup) -> dict:
    data = dict()
    return data
