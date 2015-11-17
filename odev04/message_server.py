__author__ = 'saddam'

import socket
import threading
import datetime

class ThreadClass(threading.Thread):
    def run(self):
        now = datetime.datetime.now()
        print "%s says Hello World at time: %s" % (self.getName(), now)

class myThread(threading.Thread):
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def run(self):
        '''
        now = datetime.datetime.now()
        print "%s says Hello World at time: %s" % (self.getName(), now)
        '''

    def listen(self):
        self.sock.listen(5)
        while True:
            print "Waiting for connection"
            c, addr = self.sock.accept()
            print 'Got a connection from', addr
            t = ThreadClass()
            t.start()
            c.settimeout(60)
            threading.Thread(target = self.listenToUser,args = (c,addr)).start()

    def listenToUser(self, c, addr):
        size = 1024
        while True:
            try:
                msg = c.recv(size)
                if msg:
                    response = msg
                    c.send(response)
                else:
                    raise error('Baglanti kopuk')
            except:
                c.close()
                return False

if __name__ == "__main__":
    port_num = input("Port? ")
    myThread('',port_num).listen()


