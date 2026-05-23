import requests
import sys
import queue
import threading
import argparse


argparse = argparse.ArgumentParser(description='this tool is used for bruteforcing the directory online')
argparse.add_argument('-H','--HOST',help='ENTER HOST NAME')
argparse.add_argument('-W','--words',help='ENTER WORDLIST')
argparse.add_argument('-T','--THREADS',help='ENTER NO OF THREADS')
argparse.add_argument('-E','--ext',help='ENTER EXTENSION LIKE .php,.asp')
argparse.add_argument('-F','--file',help='ENTER NAME OF THE FILE')

args = argparse.parse_args()


try:
    requests.get(args.HOST)
except Exception as e:
    print(e) 
    exit(0)



wordlist = open(args.words, 'r')

q = queue.Queue()
count =0
def buster(threadno, q):
    global count
    while not q.empty():
        url = q.get()
        try:
            response = requests.get(url , allow_redirects=False,timeout=1)
            count += 1
            print("Trying.... {}".format(count))
            if response.status_code == 200:
                a = print("[+] Directory found {}".format(url))
                with open(args.file , 'a') as f:
                    f.write(url+'\n')

        except:
            pass
        q.task_done()

for word in wordlist.read().splitlines():
    
    if not args.ext:
    
        url = args.HOST + '/' + word
    else:
        url = args.HOST + '/' + word + args.ext
    q.put(url)




for i in range(int(args.THREADS)):

    t = threading.Thread(target = buster,args=(i,q,))
    
    t.start()

q.join()



