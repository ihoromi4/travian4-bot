import json

BUILDINGS_REPR = {
    (0, "buildingsite"),
    (1, "woodcutter"),
    (2, "claypit"),
    (3, "ironmine"),
    (4, "cropland"),
    (10, 'warehouse'),
    (11, 'granary'),
    (15, "mainbuilding"),
    (16, "rallypoint"),
    (17, "marketplace"),
    (24, "townhall"),
    (25, "residence"),
    (26, "palace"),
    (33, "palisade")
}


class Language:
    def __init__(self, lang_file_path):
        self.lang_file_path = lang_file_path
        self.data = None
        self.load_data()
        self.dict_index_to_building = dict(BUILDINGS_REPR)
        self.dict_building_to_index = dict(((a, b) for a, b in BUILDINGS_REPR))

    def load_data(self):
        with open(self.lang_file_path, 'r') as file:
            self.data = json.load(file)

    def save_data(self):
        with open(self.lang_file_path, 'w') as file:
            json.dump(self.data, file)

    def set_repr_to_local_language(self, repr: str, loc_lang: str):
        if not type(repr) is str:
            raise TypeError('Type of repr must be str')
        if not type(loc_lang) is str:
            raise TypeError('Type of loc_lang must be str')
        self.data['buildings'][repr] = loc_lang

    def resource_to_int(self, resource_name):
        return self.data['resources-id'][resource_name]

    def resource_translate(self, resource_name):
        return self.data['resources'][resource_name]

    def index_to_building_repr(self, index: int):
        repr = self.dict_index_to_building.get(index, None)
        if not repr:
            raise KeyError('Language building repr no has key: {}'.format(index))
        return repr