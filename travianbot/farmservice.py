from . import farmvillage


class FarmService:
    def __init__(self, village, farms_positions: list):
        self.village = village
        self.farms = []
        for pos, troops in farms_positions:
            farm = farmvillage.FarmVillage(village, pos, troops)
            self.farms.append(farm)

    def update(self):
        for farm in self.farms:
            farm.update()
