from . import building
from . import resourcefield
from . import marketplace
from . import residence
from . import palace

building_dict = {
    "woodcutter": resourcefield.ResourceField,
    "claypit": resourcefield.ResourceField,
    "ironmine": resourcefield.ResourceField,
    "cropland": resourcefield.ResourceField,
    "marketplace": marketplace.Marketplace,
    "residence": residence.Residence,
    "palace": palace.Palace
}


def get_building_type(name):
    if name in building_dict:
        return building_dict[name]
    return building.Building
