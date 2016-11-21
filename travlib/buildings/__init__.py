from . import building
from . import resourcefield
from . import marketplace


def get_building_type(name):
    if name in ["woodcutter", "claypit", "ironmine", "cropland"]:
        return resourcefield.ResourceField
    elif name == "marketplace":
        return marketplace.Marketplace
    return building.Building
