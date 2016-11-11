import re


class Village:
    def __init__(self, account, id):
        self.account = account
        self.id = id

    def get_name(self):
        html_text = self.account.login.load_dorf1(self.id).text
        pattern = r'<div id="villageNameField" class="boxTitle">(.*)</div>'
        regex = re.compile(pattern)
        names = regex.findall(html_text)
        return names[0]
    name = property(get_name)

    def get_warehouse(self):
        html_text = self.account.login.load_dorf1(self.id).text
        pattern = r'<span class="value" id="stockBarWarehouse">(\d*)</span>'
        warehouse = int(re.findall(pattern, html_text)[0])
        return warehouse
    warehouse = property(get_warehouse)

    def get_granary(self):
        html_text = self.account.login.load_dorf1(self.id).text
        pattern = r'<span class="value" id="stockBarGranary">(\d*)</span>'
        granary = int(re.findall(pattern, html_text)[0])
        return granary
    granary = property(get_granary)

    def get_resources(self):
        html_text = self.account.login.load_dorf1(self.id).text
        pattern = r'<span id="l\d" class="value">(\d*)</span>'
        raw_resources = re.findall(pattern, html_text)
        resources = [int(p) for p in raw_resources]
        return resources
    resources = property(get_resources)

    def get_production(self):
        html_text = self.account.login.load_dorf1(self.id).text
        pattern = r'‎&#x202d;&#x202d;(\d*)&#x202c;&#x202c;'
        raw_production = re.findall(pattern, html_text)
        production = [int(p) for p in raw_production]
        return production
    production = property(get_production)
