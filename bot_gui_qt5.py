import json

from travianbot.model import Model
from travianbot.controller import Controller
from travianbot.view import View

with open('data/guiset.json') as file:
    view_settings = json.load(file)

model = Model()
view = View(view_settings)
controller = Controller(model, view)

view.show()
