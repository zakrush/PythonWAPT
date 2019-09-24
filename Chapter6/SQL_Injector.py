import requests
from threading import Thread
import sys
from termcolor import colored
import getopt

def banner():
    print("\n********************")
    print('*  SQL Injector  *')
    print("********************")

def usage():
    def usage():
        print("Usage:")
        print("         -w: url (http://somesite.com/news.php?id=FUZZ")
        print("         -i: injection strings file")
        #print("         -u: username")
        #print("         -f: dictionary file \n")
        print("example: SQL_Injector.py -w http://targetsite.com/news.php?id=FUZZ  -i common.txt\n")

def start(argv):
    banner()
    if len(sys.argv) < 2:
        usage()
        sys.exit()

    try:
        opts, args = getopt.getopt(argv, "w:i:")
    except getopt.GetoptError:
        print("Error en arguments")
        sys.exit()

    for opt, arg in opts:
        if opt == '-w':
            url = arg
        elif opt == '-i':
            dictio = arg

    try:
       f = open(dictio, "r")
       injects = f.readlines()
    except:
        print("Failed opening file: " + dictio)
        sys.exit()

    launcher(url, injects)

def launcher(url, diction):
    injected = []
    for sql_inject in diction:
        injected.append(url.replace('FUZZ', sql_inject))

    res = injector(injected)
    print("Detection results:")
    print("-------------------")

    for x in res:
        print(x.split(';'))


def injector(injected):
    errors = ['Mysql', 'error in your SQL']
    results = []

    for y in injected:
        print("[-] Testing errors: " + y)
        req = requests.get(y)

        for x in errors:
            if req.content.find(x) != -1:
                res = y + ';' + x
                results.append(res)
    return results

