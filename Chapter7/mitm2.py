import sys

def request(context, flow):
    q = flow.request.get_query() #после обновления посмотреть в дебаге, что хранится в данной переменной
    if q:
        q["isadmin"] = ["True"]
        flow.request.set_query(q)