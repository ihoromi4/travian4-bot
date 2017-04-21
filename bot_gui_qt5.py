import os
import logging
import json

if not os.path.isdir('log'):
    os.makedirs('log')

log_format = '%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s'
logging.basicConfig(format=log_format,
                    level=logging.DEBUG)
                    #filename='log/log.log')

from travianbot.model import Model
from travianbot.controller import Controller
from travianbot.view import View

with open('data/guiset.json') as file:
    view_settings = json.load(file)

with open('config.json') as file:
    config = json.load(file)

model = Model()
view = View(view_settings, config)
controller = Controller(model, view)

view.show()
