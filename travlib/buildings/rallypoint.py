from . import building


# Точка сбора
class RallyPoint(building.Building):
    def __init__(self, village_part, name, id, level):
        building.Building.__init__(self, village_part, name, id, level)
        self.eng_name = 'rallypoint'

