import json

class Language:
    def __init__(self, file_path, language, server):
        self.file_path = file_path
        self.language = language
        self.server = server
        with open(file_path, 'r') as stream:
            self.alldata = json.load(stream)
            self.data = self.alldata[language]
        self.url = self.data['url'][server]

    def resource_to_int(self, resource_name):
        return self.data['resources-id'][resource_name]

    def resource_translate(self, resource_name):
        return self.data['resources'][resource_name]
