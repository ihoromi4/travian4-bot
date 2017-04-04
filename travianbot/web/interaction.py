import json
import requests

def verification(url: str, version: tuple):
    url = url + '/api/verification'
    data = {'version': version}
    json_data = json.dumps(data)
    response = requests.post(url, data=json_data)
    if response.status_code == 200:
        data = response.json()
        return data['version_ok']
    return False

def load_accounts(url: str):
    url = url + '/api/accounts'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    raise Exception()

