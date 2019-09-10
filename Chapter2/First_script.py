import requests

payload = {'url': 'http://timebook.ru'}
r = requests.get('http://httpbin.org/redirect-to', params=payload)

print(r.status_code)