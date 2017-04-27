import json


class JSONConf:
    def __init__(self, filename: str):
        self.filename = filename

        with open(filename) as file:
            self.configuration = json.load(file)

    def save(self):
        with open(self.filename, 'w') as file:
            json.dump(self.configuration, file, indent=4)

    def __getitem__(self, item):
        return self.configuration[item]

    def __setitem__(self, key, value):
        self.configuration[key] = value

    def __contains__(self, item):
        return item in self.configuration
