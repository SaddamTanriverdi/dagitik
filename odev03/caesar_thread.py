__author__ = 'saddam'
import threading
import time

s = 3
n = 4
l = 100
a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
ca = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

for i in range(26):
    ca[s-i-1] = a[25-i]

print(a)
print(ca)

r = open('metin.txt','r+')
w = open('crypted_3_3_5.txt','w')

def cipher(str,l):
    str = r.read(l).lower()
    print "Read String is : ", str
    L = list(str)
    for i in range(l):
        for k in range(26):
            if L[i] == a[k]:
                L[i] = ca[k]
    n = ''.join(L)
    return n.upper()

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        threadLock.acquire()
        print_time(self.name, self.counter, 1)
        threadLock.release()

def print_time(threadName, delay, counter):
    while counter:
        time.sleep(delay)
        print "%s" % (threadName)
        m = cipher(str, l)
        print "Encrypted String is : ", m
        w.write(m)
        counter -= 1

threadLock = threading.Lock()
threads = []

#Create new threads & Add threads to thread list & Wait for all threads to complete
def createThread(n):
    for i in range(n):
        g = i+1
        thread = myThread(g, "Thread", g)
        thread.start()
        threads.append(thread)

def continueCrypted():
     for i in range(5):
         createThread(n)

continueCrypted()

for t in threads:
    t.join()

r.close()
w.close()
print "Exiting Main Thread"






