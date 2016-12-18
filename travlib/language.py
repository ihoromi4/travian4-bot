import json

BUILDINGS_REPR = {
    (0, "buildingsite"),
    (1, "woodcutter"),
    (2, "claypit"),
    (3, "ironmine"),
    (4, "cropland"),
    (5, 'sawmill'),
    (6, 'brickyard'),
    (7, 'ironfoundry'),
    (8, 'grainmill'),
    (9, 'bakery'),
    (10, 'warehouse'),
    (11, 'granary'),

    (13, 'smithy'),
    (14, 'tournamentsquare'),
    (15, "mainbuilding"),
    (16, "rallypoint"),
    (17, "marketplace"),
    (18, 'embassy'),
    (19, 'barracks'),
    (20, 'stable'),
    (21, 'workshop'),
    (22, 'academy'),
    (23, 'cranny'),
    (24, "townhall"),
    (25, "residence"),
    (26, "palace"),
    (27, 'treasury'),
    (28, 'tradeoffice'),

    (31, 'wall'),
    (32, 'earthwall'),
    (33, "palisade"),
    (34, 'stonemasonslodge'),
    (35, 'brewery'),
    (36, 'trapper'),
    (37, 'herosmansion'),
    (38, 'greatwarehouse'),
    (39, 'greatgranary')
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