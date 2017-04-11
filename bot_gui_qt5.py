from travianbot.model import Model
from travianbot.controller import Controller
from travianbot.view import View

view_settings = {
    'mainwindow_title': 'Auto-Travian',
    'icon_path': 'data/travbot.png',
    'ui_dir': 'data/ui',
    'ui_mainwindow': 'data/ui/mainwindow.ui'
}

model = Model()
view = View(view_settings)
controller = Controller(model, view)

view.show()
