from . import building
from . import marketplace
from . import palace
from . import residence
from . import resourcefield
from . import townhall

building_dict = {
    "woodcutter": resourcefield.Woodcutter,
    "claypit": resourcefield.Claypit,
    "ironmine": resourcefield.Ironmine,
    "cropland": resourcefield.Cropland,
    "marketplace": marketplace.Marketplace,
    "residence": residence.Residence,
    "palace": palace.Palace,
    "townhall": townhall.TownHall
}


def get_building_type(name):
    if name in building_dict:
        return building_dict[name]
    return building.Building
