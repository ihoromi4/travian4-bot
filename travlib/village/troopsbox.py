
class TroopsBox:
    def __init__(self, village):
        self.village = village

    def get_rallypoint(self):
        return self.village.inner.get_building('rallypoint')
    rallypoint = property(get_rallypoint)

    def reinforcement(self):
        pass

    def attack_normal(self):
        pass

    def attack_raid(self, pos, troops):
        self.rallypoint.send_troops(pos, troops)
