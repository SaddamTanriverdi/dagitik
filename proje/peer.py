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
--------------------Peer-Server---------------------------------------------------------------------------------------
'''

PATCHSIZE = 128
UPDATE_INTERVAL = 600
THREADNUM = 4
psdataList = []

class wThread (threading.Thread):
    def __init__(self, threadID, name, c, addr, psQueue, CONNECT_POINT, counter ):
        threading.Thread.__init__(self)
        self.name = name
        self.c = c
        self.threadID = threadID
        self.counter = counter
        self.addr = addr
        self.psQueue = psQueue
        self.CONNECT_POINT = CONNECT_POINT
        self.pData = ""

    def run(self):
        self.lQueue.put("Starting " + self.name)
        while True:
            queue_message = str(self.psQueue.get())
            if queue_message[0:5] not in psdataList:
                sendMsg = queue_message[6:]
            else:
                sendMsg = queue_message
            self.c.send(sendMsg)
        self.lQueue.put("Finished " + self.name + "\n")

class rThread (threading.Thread):
    def __init__(self, threadID, name, c, addr, ip, port, psQueue, CONNECT_POINT, counter):
        threading.Thread.__init__(self)
        self.nickname = ""
        self.name = name
        self.threadID = threadID
        self.counter = counter
        self.ip = ip
        self.port = port
        self.c = c
        self.addr = addr
        self.CONNECT_POINT = CONNECT_POINT
        self.psQueue = psQueue

    def parser(self,data):
        data = data.strip()
        loggerMsg = " "
        #data sekli bozuksa
        if data[0:5] != ""+ c.recv(1024).decode('UTF-8') or len(data)<5:
            response = "CMDER"
            psdataList.append(response)
            self.c.send(response)
            return response

        if not self.nickname and data[0:5] == "REGME" and data[6:21] != "" and data[22:27] != ""  :
            psdataList.append("REGME")
            nickname = data[6:21]
            ip = data[6:21]
            port = data[22:27]
            response = "REGWA"
            self.c.send(response)
            psdataList.append("REGWA")
            self.psQueue.put(self.port + ":" + "W")
            self.CONNECT_POINT[self.nickname] = self.psQueue
            if nickname != "":
                if nickname not in self.CONNECT_POINT:
                    self.nickname = nickname
                    self.ip = ip
                    self.port = port
                    self.nQueue.put(self.port + ":" + "S")
                    self.CONNECT_POINT[self.nickname] = self.psQueue
                    self.CONNECT_POINT.update()
                    loggerMsg = self.nickname + "Has Joined."
                    self.lQueue.put(self.nickname + " Has Joined.")
                    response = "REGOK" + nickname
                    psdataList.append("REGOK")
                    self.c.send(response)
                    return response
                else:
                    # kullanici reddedilecek
                    response = "REGER" + nickname
                    psdataList.append("REGER")
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
                psdataList.append("HELLO")
                response = "SALUT"
                psdataList.append("SALUT")
                self.c.send(response)
                return response

            elif data[0:5] == "CLOSE":
                psdataList.append("CLOSE")
                #fihristten sil
                CONNECT_POINT.__delitem__(self.nickname)
                #log gönder
                self.lQueue.put(self.nickname + " Has closed.")
                response = "BUBYE " + self.nickname
                psdataList.append("BUBYE")
                self.c.send(response)
                #bağlantıyı sil
                self.c.close()
                return response

            elif data[0:5] =="GETNL":
                psdataList.append("GETNL")
                cLogin = ""
                response = "NLIST BEGIN"
                self.c.send(response)
                for k in self.CONNECT_POINT.keys():
                    t = time.ctime()
                    cLogin += k + "<ip>: " +self.ip + "<port>: " +self.port + "<time>: "+ str(t) + "<type>: "+ self.name
                    response = "NLIST " + cLogin[:-1]
                    self.c.send(response)
                response = "NLIST END"
                self.c.send(response)
                return response

            elif data[0:5] == "FUNLS":
                psdataList.append("FUNLS")
                response = "FUNLS BEGIN"
                self.c.send(response)
                response = "<Functionname>: <parameter_intervals>"
                self.c.send(response)
                m = 1
                for k in self.functionList.keys():
                    response ="Function %s:" %(m) + " " + k +","+ " " + functionList.values(m-1) + "\n"
                    m = m+1
                    self.c.send(response)
                response = "FUNLS END"
                self.c.send(response)
                return response

            elif data[0:5] == "FUNRQ":
                psdataList.append("FUNRQ")
                funcname = data[6:]
                for funcname in self.functionList.keys():
                    if funcname not in self.self.functionList.keys():
                        response = "FUNNO" + funcname
                psdataList.append("FUNNO")
                self.c.send(response)
                m = 1
                for funcname in self.functionList.keys():
                    if funcname in self.self.functionList.keys():
                        response = "FUNYS" + funcname + ":" + " "  + functionList.values(m-1) + "\n"
                    m = m+1
                    psdataList.append("FUNYS")
                    self.c.send(response)
                    return response

            elif data[0:5] == "EXERQ":
                psdataList.append("EXERQ")
                #<functionname>:<parameters>:<num> sayma sayısı:<md5sum> 32 karekter:<udata>
                funcname = data[6:data.indexOf(":")]
                parameters = data[data.indexOf(":")+1:data.indexOf(":")]
                num = data[data.indexOf(":")+1:data.indexOf(":")]
                md5sum = data[data.indexOf(":")+1:data.indexOf(":")+33]
                udata = data[data.indexOf(":")+33:]
                m = 0
                for funcname in self.functionList.keys():
                    if funcname in self.self.functionList.keys():
                        response = "EXEOK" + " " + md5sum + ":" + " " + num
                        self.c.send(response)
                        return response
                    else:
                        m = 1
                if m == 1:
                    response = "EXEDS" + " " + md5sum + ":" + " " + num
                    self.c.send(response)
                    return response

                for funcname in self.functionList.keys():
                    if funcname in self.self.functionList.keys():
                        self.pData = funcname(parameters)

            elif data[0:5]  == "PATCH":
                md5sum = data[6:data.indexOf(":")]
                num = data[data.indexOf(":")+1:data.indexOf(":")]
                pdata = data[data.indexOf(":")+33:]

                if pdata == self.pData:
                    response = "PATYS" + " " + md5sum + ":" + " " + num
                    self.c.send(response)
                    return response
                else:
                    response = "PATNO" + " " + md5sum + ":" + " " + num
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
            self.psQueue.put(response)
            #lock mekanizması unutma
            threadLock.acquire()
            print_time(self.name, self.counter, 1)
            threadLock.release()

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
        reedThread = rThread(g, "rThread", c, addr, ip, port, psQueue, CONNECT_POINT, g)
        reedThread.start()
        clients.append(reedThread)

        writeThread = wThread( g, "wThread", c, addr, psQueue, CONNECT_POINT, g )
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
    clientsNumber = 0
    CONNECT_POINT = {}
    functionList = {}

    while 1:
        psQueue = Queue.Queue()
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
        createThread(THREADNUM)

        for t in clients:
            t.join()

        rThread.close()
        wThread.close()
        print "Exiting Main Thread of Negotiator-server"


'''
------------------Peer_client-----------------------------------------------------------------------------------------
'''

pcdataList = []

class pcReadThread(threading.Thread):
    def __init__(self, name, ip, port, c, ncQueue, pcfunctionList):
        threading.Thread.__init__(self)
        self.name = name
        self.c = c
        self.nickname = " "
        self.ncQueue = ncQueue
        self.pcfunctionList = pcfunctionList
        self.ip = ip
        self.port = port

    def incoming_parser(self, data):
        data = data.strip()
        if len(data) == 0:
            return 1
        if data[0:5] != ""+ c.recv(1024).decode('UTF-8') or len(data)<5:
            response = "REGER"
            pcdataList.append(response)
            return response
        elif data[0:5] == "REGOK":
            type = data[6:7]
            response = "HELLO"
            pcdataList.append(response)
            return response
        elif data[0:5] == "BUBYE":
            response = "CLOSE"
            pcdataList.append(response)
            return response
        elif data[0:12] == "FUNLS BEGIN":
            while data != "FUNLS END":
                funcname = data[data.indexOf(":"):data.indexOf(",")]
                parameters = data[data.indexOf(","):]
                self.pcfunctionList[funcname] = parameters
        elif data[0:5] == "FUNNO":
            response = "FUNNO"
            pcdataList.append(response)
        elif data[0:5] == "FUNYS":
            while data == "FUNYS":
                funcname = data[6:data.indexOf(":")]
                parameters = data[data.indexOf(":")+1:]
            response = "FUNYS"
            pcdataList.append(response)
        elif data[0:5] == "EXEOK":
            md5sum = data[6:data.indexOf(":")]
            num = data[data.index(":")+1:]
            response = "EXEOK"
            pcdataList.append(response)
        elif data[0:5] == "EXEDS":
            md5sum = data[6:data.indexOf(":")]
            num = data[data.index(":")+1:]
            response = "EXEDS"
            pcdataList.append(response)
        elif data[0:5] == "PATYS":
            md5sum = data[6:data.indexOf(":")]
            num = data[data.index(":")+1:]
            response = "PATYS"
            pcdataList.append(response)
        elif data[0:5] == "PATNO":
            md5sum = data[6:data.indexOf(":")]
            num = data[data.index(":")+1:]
            response = "PATNO"
            pcdataList.append(response)
        else:
            response = "CMDER"
            pcdataList.append(response)
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


class pcWriteThread(threading.Thread):
    def __init__(self, name, ip, port, c, pcQueue):
        threading.Thread.__init__(self)
        self.name = name
        self.c = c
        self.pcQueue = pcQueue
        self.ip = ip
        self.port = port

    def run(self):
        print("Starting "+self.name)
        while True:
            q_msg = str(self.pcQueue.get())
            try:
                if q_msg == "BUBYE":
                    break
                elif not q_msg[0:5] in pcdataList:
                    msg = q_msg[6:]
                else:
                    msg = q_msg
                    print("Queue message: "+ q_msg)
                    self.c.send(str(msg))
            except socket.error:
                self.c.close()
                break
        print("Finished "+self.name)

def pcPrint_time(threadName, delay, counter):
    while counter:
        time.sleep(delay)
        print "%s" % (threadName)
        counter -= 1

#Create new threads & Add threads to thread list & Wait for all threads to complete
def pcCreateThread(n):
    for i in range(n):
        g = i+1
        ip = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
        port = random.randint(1, 65535)
        reedThread = rThread("ReadThread", ip, port, s, pcQueue, pcfunctionList)
        reedThread.start()
        clients.append(reedThread)

        writeThread = wThread("WriteThread", ip, port, s, pcQueue)
        writeThread.start()
        clients.append(writeThread)

s = socket.socket()
host =str(sys.argv[1])
port =66666
s.connect((host,port))
print(" we have a connaction:")
pcfunctionList = {}

pcQueue = Queue.Queue()

# start threads
threadLock = threading.Lock()
pcCreateThread(THREADNUM)

for t in clients:
    t.join()

rThread.join()
wThread.join()
s.close()
