import sys

def request(flow):
    q = flow.request.query #после обновления посмотреть в дебаге, что хранится в данной переменной
    if q:
        q["id"] = "10"
        q["isadmin"] = "True"
       # flow.request.query(q)