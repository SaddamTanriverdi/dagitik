__author__ = 'saddam'

import socket
import threading

class readThread(threading.Thread):
    def run(self):
        print "response: ", s.recv(1024)

class writeThread(threading.Thread):
    def run(self):
        msg = raw_input("message: ")
        s.send(msg)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = raw_input("Server hostname? ")
port = input("Server port? ")
s.connect((host,port))

'''
rThread = readThread()
rThread.start()
wThread = writeThread()
wThread.start()

'''

while True:
    msg = raw_input("message: ")
    s.send(msg)
    print "response: ", s.recv(1024)
    if msg == 'end':
        break

