from . import building
from . import resourcefield
from . import marketplace

_lang = None


def set_lang(lang_data):
    global _lang
    _lang = lang_data


def get_building_type(name):
    if not _lang:
        raise AttributeError("not initialized 'language'")
    elif name in _lang['resource-field']:
        return resourcefield.ResourceField
    elif name == _lang['marketplace']:
        return marketplace.Marketplace
    return building.Building
