import socket
import threading
import Queue
import time
import sys
import os
from itertools import cycle
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import random

'''
------------------Negotiator_server------------------------------------------------------------------------------------
'''
PATCHSIZE = 128
UPDATE_INTERVAL = 600
THREADNUM = 4

dataList = []

class wThread (threading.Thread):
    def __init__(self, threadID, name, c, addr, nQueue, CONNECT_POINT_LIST, counter ):
        threading.Thread.__init__(self)
        self.name = name
        self.c = c
        self.threadID = threadID
        self.counter = counter
        self.addr = addr
        self.nQueue = nQueue
        self.CONNECT_POINT_LIST = CONNECT_POINT_LIST
    def run(self):
        self.lQueue.put("Starting " + self.name)
        while True:
            queue_message = str(self.nQueue.get())
            if queue_message[0:5] not in dataList:
                sendMsg = queue_message[6:]
            else:
                sendMsg = queue_message
            self.c.send(sendMsg)
        self.lQueue.put("Finished " + self.name + "\n")

class rThread (threading.Thread):
    def __init__(self, threadID, name, c, addr, ip, port, nQueue, CONNECT_POINT_LIST, counter):
        threading.Thread.__init__(self)
        self.nickname = ""
        self.name = name
        self.threadID = threadID
        self.counter = counter
        self.ip = ip
        self.port = port
        self.c = c
        self.addr = addr
        self.CONNECT_POINT_LIST = CONNECT_POINT_LIST
        self.nQueue = nQueue

    def parser(self,data):
        data = data.strip()
        loggerMsg = " "
        #data sekli bozuksa
        if data[0:5] != ""+ c.recv(1024).decode('UTF-8') or len(data)<5:
            response = "CMDER"
            dataList.append(response)
            self.c.send(response)
            return response
        if not self.nickname and data[0:5] == "REGME" and data[6:21] != "" and data[22:27] != "":
            dataList.append("REGME")
            nickname = data[6:21]
            ip = data[6:21]
            port = data[22:27]
            response = "REGWA"
            self.c.send(response)
            dataList.append("REGWA")
            self.nQueue.put(self.port + ":" + "W")
            self.CONNECT_POINT_LIST[self.nickname] = self.nQueue
            if nickname != "":
                if nickname not in self.CONNECT_POINT_LIST:
                    self.nickname = nickname
                    self.ip = ip
                    self.port = port
                    self.nQueue.put(self.port + ":" + "S")
                    self.CONNECT_POINT_LIST[self.nickname] = self.nQueue
                    self.CONNECT_POINT_LIST.update()
                    response = "REGOK" + nickname
                    dataList.append("REGOK")
                    self.c.send(response)
                    return response
                else:
                    # kullanici reddedilecek
                    response = "REGER" + nickname
                    dataList.append("REGER")
                    self.c.send(response)
                    return response
            else:
                response = "REGER"
                self.c.send(response)
                # baglantiyi kapat
                self.c.close()
                return response
        elif self.nickname != " ":
            if data[0:5] =="HELLO":
                dataList.append("HELLO")
                response = "SALUT"
                dataList.append("SALUT")
                self.c.send(response)
                return response
            elif data[0:5] == "CLOSE":
                dataList.append("CLOSE")
                #fihristten sil
                CONNECT_POINT_LIST.__delitem__(self.nickname)
                #log gönder
                self.lQueue.put(self.nickname + " Has closed.")
                response = "BUBYE " + self.nickname
                dataList.append("BUBYE")
                self.c.send(response)
                #bağlantıyı sil
                self.c.close()
                return response
            elif data[0:5] =="GETNL":
                dataList.append("GETNL")
                cLogin = ""
                response = "NLIST BEGIN"
                self.c.send(response)
                for k in self.CONNECT_POINT_LIST.keys():
                    t = time.ctime()
                    cLogin += k + "<ip>: " +self.ip + "<port>: " +self.port + "<time>: "+ str(t) + "<type>: "+ self.name + "\n"
                    response = "NLIST " + cLogin[:-1]
                    self.c.send(response)
                response = "NLIST END"
                self.c.send(response)
                return response
            else:
                response = "REGER"
                self.c.send(response)
                # baglantiyi kapat
                self.c.close()
                return response
        else:
            response = "REGER"
            self.csend(response)
            return response

    def run(self):
        self.lQueue.put("Starting " + self.name)
        while True:
            incoming_data = self.c.recv(1024)
            msg = self.parser(incoming_data)
            self.lQueue.put(msg)
            #istemciye cevap hazirla.
            response = self.parser(incoming_data)
            #cevap veya cevaplari göndermek üzere
            #threadQueue'ya yaz
            self.nQueue.put(response)
            #lock mekanizması unutma
            threadLock.acquire()
            print_time(self.name, self.counter, 1)
            threadLock.release()
        self.lQueue.put("Exiting " + self.name)


def print_time(threadName, delay, counter):
    while counter:
        time.sleep(delay)
        print "%s" % (threadName)
        counter -= 1

#Create new threads & Add threads to thread list & Wait for all threads to complete
def createThread(n):
    for i in range(n):
        g = i+1
        ip = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
        port = random.randint(1, 65535)
        reedThread = rThread(g, "rThread", c, addr, ip, port, nQueue,   CONNECT_POINT_LIST, g)
        reedThread.start()
        clients.append(reedThread)

        writeThread = wThread( g, "wThread", c, addr, nQueue,   CONNECT_POINT_LIST, g )
        writeThread.start()
        clients.append(writeThread)

if __name__ == '__main__':

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    host = socket.gethostname()
    port = 66666
    s.bind((host, port))
    s.listen(3)

    clients = []
    functionList = []
    clientsNumber = 0
    CONNECT_POINT_LIST = {}

    while 1:
        nQueue = Queue.Queue()
        print "Waiting for Connections"
        try:
            c, addr = s.accept()
            c.settimeout(1)
        except KeyboardInterrupt:
            s.close()
            for sock in clients:
                sock.close()
            break
        clients.append(c)
        clientsNumber += 1
        threadLock = threading.Lock()
        createThread(5)

        for t in clients:
            t.join()

        rThread.close()
        wThread.close()
        print "Exiting Main Thread of Negotiator-server"

'''
------------------Negotiator_client-----------------------------------------------------------------------------------
'''

ncdataList = []

class ncReadThread(threading.Thread):
    def __init__(self, name, c, ncQueue):
        threading.Thread.__init__(self)
        self.name = name
        self.c = c
        self.nickname = " "
        self.ncQueue = ncQueue
    def incoming_parser(self, data):
        data = data.strip()
        if len(data) == 0:
            return 1
        if data[0:5] != ""+ c.recv(1024).decode('UTF-8') or len(data)<5:
            response = "CMDER"
            ncdataList.append(response)
            return response
        elif data[0:5] == "SALUT":
            type = data[6:7]
            response = "HELLO"
            ncdataList.append(response)
            return response
        elif data[0:5] == "BUBYE":
            response = "CLOSE"
            ncdataList.append(response)
            return response
        else:
            response = "CMDER"
            ncdataList.append(response)
            return response
    def run(self):
        print("Starting "+self.name)
        while True:
            data = self.c.recv(1024)
            msg = self.incoming_parser(data)
            self.ncQueue.put(" " + msg + "\n")
            if(msg == 1):
                self.c.close()
                break
        print("Finished "+self.name)

class ncWriteThread(threading.Thread):
    def __init__(self, name, c, ncQueue):
        threading.Thread.__init__(self)
        self.name = name
        self.c = c
        self.ncQueue = ncQueue
    def run(self):
        print("Starting "+self.name)
        while True:
            q_msg = str(self.ncQueue.get())
            try:
                if q_msg == "REGER" or q_msg == "CMDER":
                    break
                elif not q_msg[0:5] in ncdataList:
                    msg = q_msg[6:]
                else:
                    msg = q_msg
                    print("Queue message: "+ q_msg)
                    self.c.send(str(msg))
            except socket.error:
                self.c.close()
                break
        print("Finished "+self.name)

def ncPrint_time(threadName, delay, counter):
    while counter:
        time.sleep(delay)
        print "%s" % (threadName)
        counter -= 1

#Create new threads & Add threads to thread list & Wait for all threads to complete
def ncCreateThread(n):
    for i in range(n):
        g = i+1
        ip = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
        port = random.randint(1, 65535)
        reedThread = rThread("ReadThread", ip, port, s, ncQueue)
        reedThread.start()
        clients.append(reedThread)

        writeThread = wThread("WriteThread", ip, port, s, ncQueue )
        writeThread.start()
        clients.append(writeThread)


s = socket.socket()
host =str(sys.argv[1])
port =66666
s.connect((host,port))
print(" we have a connaction:")


ncQueue = Queue.Queue()

# start threads
threadLock = threading.Lock()
ncCreateThread(THREADNUM)

for t in clients:
    t.join()

rThread.join()
wThread.join()
s.close()