from travianbot.model import Model
from travianbot.controller import Controller
from travianbot.view import View


url = 'http://ts5.travian.ru/'
name = 'broo'
password = 'wA4iN_tYR'

user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'
headers = {'User-Agent': user_agent}

account_settings = {
    'url': url,
    'name': name,
    'password': password,
    'headers': headers
}

view_settings = {
    'mainwindow_title': 'Auto-Travian',
    'icon_path': 'data/travbot.png',
    'ui_dir': 'data/ui',
    'ui_mainwindow': 'data/ui/mainwindow.ui'
}

model = Model()
view = View(view_settings)
controller = Controller(model, view)

# model.open_service(account_settings)
model.run()
view.show()
