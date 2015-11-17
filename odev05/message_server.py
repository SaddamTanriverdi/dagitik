import socket
import threading
import Queue
import time
import sys
import os
from itertools import cycle

fihrist = []
host = ''
port = 50000

class wThread (threading.Thread):
    def __init__(self, name, c, addr, tQueue, lQueue ):
        threading.Thread.__init__(self)
        self.name = name
        self.c = c
        self.addr = addr
        self.lQueue = lQueue
        self.tQueue = tQueue
    def run(self):
        self.lQueue.put("Starting " + self.name)
        while True:
            try:
                data = c.recv(4096)
                peer = c.getpeername()
            except self.c.timeout:
                continue
            except self.c.error:

                print "Server shutdown"
                return
            except:
                error=None
                print "A disconnect by " + str(peer)
                if error:
                    msg = str(peer) + " has exited -- " + error + "\r\n"
                else:
                    msg = str(peer) + " has exited\r\n"
                tQueue.writer(msg)
                break

            if self.tQueue.qsize() > 0:
                msg = self.tQueue.get()
                # gonderilen ozel mesajsa
                if not tQueue.empty():
                    self.c.send(msg)
                    message_to_send = "MSG " + msg
                # genel mesajsa
                elif msg[1]:
                    reading = tQueue.reader()
                    if reading == None:
                        return 1
                    else:
                        peer = c.getpeername()
                        print "Got connection from ", peer
                        msg = str(peer) + " has joined\r\n"
                        tQueue.writer(msg)
                        for (last, timeStmp, msg) in reading:
                            sock.send("At %s -- %s" % (time.asctime(timeStmp), msg))
                        message_to_send = "SAY " + last
                        return last

                # hicbiri degilse sistem mesajidir
                else:
                    msag = "system msg"
                    message_to_send = "SYS " + msag
        self.lQueue.put("Exiting " + self.name)

class rThread (threading.Thread):
    def __init__(self, name, c, addr, lQueue, tQueue, fihrist):
        threading.Thread.__init__(self)
        self.nickname = name
        self.c = c
        self.addr = addr
        self.lQueue = lQueue
        self.fihrist = fihrist
        self.tQueue = tQueue

    def parser(self,data):
        data = data.strip()
        # henuz login olmadiysa
        if not self.nickname and not data[0:3] == "USR":
            response = "LOGOUT"
            self.csend(response)
            return 0
        #data sekli bozuksa
        if data[0:3] != ""+ c.recv(1024).decode('UTF-8'):
            response = "ERR"
            self.csend(response)
            return 0
        if data[0:3] == "USR":
            nickname = data[4:]
            if not len(data):
                fihrist.__add__(self.nickname,tQueue)
                response = "HEL " + nickname
                self.csend(response)
                self.fihrist.update()
                self.lQueue.put(self.nickname + " has joined.")
                return 0
            else:
                # kullanici reddedilecek
                response = "REJ" + nickname

                # baglantiyi kapat
                self.csself.csend(response)oc.close()
                return 1
        elif data[0:3] == "QUI":
            response = "BYE " + self.nickname
            self.csend(response)
            #fihristten sil
            fihrist.__delitem__(self.nickname,tQueue)
            #log gönder
            self.lQueue.put(self.nickname + " has deleted.")
            #bağlantıyı sil
            self.csoc.close()
        elif data[0:3] =="LSQ":
            response = "LSA " + self.nickname
            self.csend(response)
        elif data[0:3] =="TIC":
            response = "TAC"
            self.csend(response)
        elif data[0:3] =="SAY":
            response = "SOK"
            self.csend(response)
        elif data[0:3] =="MSG":
            response = "MSG " + data
            self.csend(response)
            if not self.nickname in self.fihrist.keys():
                response = "MNO"
            else:
                queue_message = (to_nickname, self.nickname, message)
                #gönderilecek threadQueueyu fihristten alip icine yaz

                self.fihrist[to_nickname].put(queue_message)
                response = "MOK"
            self.csend(response)
        else:
            # Bir seye uymadiysa protokol hatası verilecek
            response = "ERR"
            self.csend(response)

    def run(self):
        self.lQueue.put("Starting " + self.name)
        while True:
            parser(self)

            queue_message = parser(incoming_data)

            #istemciye cevap hazirla.

            #cevap veya cevaplari göndermek üzere
            #threadQueue'ya yaz
            #lock mekanizması unutma

         self.lQueue.put("Exiting " + self.name)


class LoggerThread (threading.Thread):
    def __init__(self, name, logQueue, logFileName):
        threading.Thread.__init__(self)
        self.name = name
        self.IQueue = logQueue
        #dosyayı appendable olarak aç
        self.fid = logFileName
    def log(self,message):
        #gelen mesajı zamanla beraber bastir
        t = time.ctime()
        self.fid.write(t + ...)
        self.fid.flush()
    def run(self):
        self.log("Starting " + self.name)

        while True:
            # IQueue'da yeni mesaj varsa
            # self.log() metodunu cagir

            to_be_logged =
            self.log(to_be_logged)

        self.log("Exiting" + self.name)
        self.fid.close()


if __name__ == '__main__':
    clients = []
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(3)

    while 1:
        tQueue = Queue.Queue()
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

        rThread(c,addr,tQueue)
        rThread.start()

        wThread()
        wThread.start()

