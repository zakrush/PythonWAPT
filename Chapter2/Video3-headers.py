import requests

myheaders = {'User-agent':'Iphone 6'}
r = requests.get('http://httpbin.org/ip', headers=myheaders) #, data={'name':'packt'})
print(r.url)
print('Status code:')
print('\t [-]' + str(r.status_code) + '\n')

print('Server headers')
print('****************************************')
for x in r.headers:
    print('\t' + x + ' : ' + r.headers[x])
print('****************************************\n')

print("Content:\n")
print(r.text)