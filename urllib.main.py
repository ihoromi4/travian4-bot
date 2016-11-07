import os
from os import path

import urllib
from urllib import request

import http
from http import cookiejar

# user data
LOGIN = 'broo'
PASSWORD = '1994igor'

# urls
URL_LOGIN = "http://ts5.travian.ru/login.php"
DORF1="dorf1.php"
DORF2="dorf2.php"

# cookie
COOKIEFILE = 'travian.cookie'
cookie = cookiejar.LWPCookieJar()
if path.isfile(COOKIEFILE):
    cookie.load(COOKIEFILE)

# headers
user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'
headers = { 'User-Agent' : user_agent }

user_data = {} # {"account" : LOGIN, "password" : PASSWORD}
params = urllib.parse.urlencode(user_data).encode('utf-8')

request_ = request.Request(URL_LOGIN, params, headers, method='POST')

handler_cookies = request.HTTPCookieProcessor(cookie)
handler_auth = urllib.request.HTTPBasicAuthHandler()
handler_auth.add_password(realm='PDQ Application',
                          uri=URL_LOGIN,
                          user=LOGIN,
                          passwd=PASSWORD)

opener = request.build_opener(handler_cookies, handler_auth)
response = opener.open(request_, params) # open(url, data=None[, timeout])

print(response.status, response.reason)

text = response.read().decode('utf-8')
with open('index.html', 'w') as stream:
    stream.write(text)

