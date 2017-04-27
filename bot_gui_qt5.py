import os
import logging
import json

if not os.path.isdir('log'):
    os.makedirs('log')

log_format = '%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s'
log_file = None  # 'log/log.log'
logging.basicConfig(format=log_format,
                    level=logging.DEBUG,
                    filename=log_file)

from travianbot.model import Model
from travianbot.controller import Controller
from travianbot.view import View

config_path = 'config.json'
with open(config_path) as file:
    config = json.load(file)

ui_config_path = os.path.join(config['config_dir'], config['ui_config'])
with open(ui_config_path) as file:
    view_config = json.load(file)

profiles_config_path = os.path.join(config['config_dir'], config['profiles_config'])
with open(profiles_config_path) as file:
    profiles_config = json.load(file)

model = Model()
view = View(view_config, profiles_config)
controller = Controller(model, view)
# controller.load_accounts(profiles_config[0]['accounts'])

view.show()
