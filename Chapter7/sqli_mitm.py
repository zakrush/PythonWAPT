import sys
import requests
from urllib.parse import urlparse
from copy import deepcopy

def injector(url):
    errors = ['Mysql', 'error in your SQL']
    injections = ['\'', '\"', ';--']
    f = open('sqli_results.txt', 'a+')
    a = urlparse(url)
    query = a.query.split('&')
    qlen = len(query)
    while qlen != 0:
        querys = deepcopy(query)
        querys[qlen-1] = querys[qlen-1].split('=')[0] + '=FUZZ'
        newq = '&'.join(querys)
        url_to_test = a.scheme + '://' + a.netloc + a.path + '?' + newq
        qlen -= 1
        for inj in injections:
            req = requests.get(url_to_test.replace('FUZZ',inj))
            for err in errors:
                if req.text.find(err) != -1:
                    result = req.url + ';' + err + '; INJECT IS ' + inj
                    f.write(result + '\n')
    f.close()

def request(flow):
    q = flow.request.query
    print(q)
    if q:
        injector(flow.request.url)


