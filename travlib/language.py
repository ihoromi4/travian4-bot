import json


class Language:
    def __init__(self, lang_file_path):
        self.lang_file_path = lang_file_path
        self.data = None
        self.load_data(lang_file_path)

    def load_data(self, lang_file_path):
        with open(lang_file_path, 'r') as stream:
            self.data = json.load(stream)

    def resource_to_int(self, resource_name):
        return self.data['resources-id'][resource_name]

    def resource_translate(self, resource_name):
        return self.data['resources'][resource_name]
