import os
from os import path

import urllib
from urllib import request
import http
from http import cookiejar

LOGIN = 'broo'
PASSWORD = '1994igor'

URL_LOGIN = "http://ts5.travian.ru/login.php"
DORF1="dorf1.php"
DORF2="dorf2.php"

COOKIEFILE = 'travian.cookie'
cookie = cookiejar.LWPCookieJar()
if path.isfile(COOKIEFILE):
    cookie.load(COOKIEFILE)

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = { 'User-Agent' : user_agent }

user_data = {"name":LOGIN, "password":PASSWORD}
params = urllib.parse.urlencode(user_data).encode('utf-8')
print(params)

opener = request.build_opener(request.HTTPCookieProcessor(cookie))
response = opener.open(URL_LOGIN, params, headers)

print(response.status, response.reason)

text = response.read().decode('utf-8')
with open('index.html', 'w') as stream:
    stream.write(text)
#conn.close()
