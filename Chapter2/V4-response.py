import requests

url = 'http://httpbin.org/redirect-to'
payload = {'url':'http://bing.com'}
r = requests.get(url, params=payload)

print(r.url)
print('*************************************')
print('Response code: ' + str(r.status_code))
print('*************************************')
for elem in r.history:
    print(str(elem.status_code) + ' : ' + elem.url)