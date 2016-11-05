import urllib
from urllib import request
import http
from http import cookiejar

LOGIN = 'broo'
PASSWORD = '1994igor'

URL = "ts5.travian.ru"
DORF1="dorf1.php"
DORF2="dorf2.php"

user_data = {"name":LOGIN, "password":PASSWORD}
params = urllib.parse.urlencode(user_data)
#headers = 
conn = http.client.HTTPConnection(URL)
conn.request('POST', '', params)
response = conn.getresponse()
print(response.status, response.reason)
text = response.read().decode('utf-8')
with open('index.html', 'w') as stream:
    stream.write(text)
conn.close()
