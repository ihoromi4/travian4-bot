from ..model import Model
from ..view import View

url = 'http://ts5.travian.ru/'
username = 'broo'
password = 'wA4iN_tYR'

user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'
headers = {'User-Agent': user_agent}

account_settings = {
    'url': url,
    'username': username,
    'password': password,
    'headers': headers
}


class Controller:
    """ Контроллер. Отвечает за ввод пользователя """

    def __init__(self, model: Model, view: View):
        self.model = model
        self.view = view

        self.view.on_new_account.on(self.open_service)

    def open_service(self):
        self.model.open_service(account_settings)

    def load_accounts(self, accounts_config: list):
        for config in accounts_config:
            self.view.add_account_card(config)
