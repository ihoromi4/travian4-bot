import os
import logging
import json

from travianbot import jsonconf

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

config = jsonconf.JSONConf(config_path)

ui_config_path = os.path.join(config['config_dir'], config['ui_config'])
view_config = jsonconf.JSONConf(ui_config_path)

profiles_config_path = os.path.join(config['config_dir'], config['profiles_config'])
profiles_config = jsonconf.JSONConf(profiles_config_path)

model = Model()
view = View(view_config, profiles_config)
controller = Controller(model, view)
# controller.load_accounts(profiles_config[0]['accounts'])

view.show()
