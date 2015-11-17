import sys
import socket
import threading
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import Queue
import time

class ReadThread(threading.Thread):
    def __init__(self, name, c, tQueue, app):
        threading.Thread.__init__(self)
        self.name = name
        self.c = c
        self.nickname = " "
        self.tQueue = tQueue
        self.app = app

    def incoming_parser(self, data):
        data = data.strip()

        if len(data) == 0:
            return 1

        if len(data) > 3 and not data[0:3] == "":
            response = "ERR"
            self.csoc.send(response)
            return
        rest = data[4:]

        if data[0:3] == "BYE":
            response = "BYE"
            self.csend(response)

        if data[0:3] == "ERL":
            response = "ERL"
            self.csend(response)
        if data[0:3] == "HEL":
            response = "HEL"
            self.csend(response)
        if data[0:3] == "REJ":
            response = "REJ"
            self.csend(response)

        if data[0:3] == "MNO":
            response = "MOK"
            self.csend(response)
        if data[0:3] == "MSG":
            response = "MSG " + data
            self.csend(response)
        if data[0:3] == "SAY":
            response = "SOK"
            self.csend(response)

        if data[0:3] == "SYS":
            response = "SYS"
            self.csend(response)

        if data[0:3] == "LSA":
            splitted = rest.split(":")
            msg = "-Server- Registered nicks: "
            for i in splitted:
                msg += i + ","
            msg = msg[:-1]


            self.app.cprint(msg)


    def run(self):
        while True:
            data = self.c.recv(1024)
            incoming_parser(self, data)



class WriteThread(threading.Thread):
    def __init__(self, name, c, tQueue):
        threading.Thread.__init__(self)
        self.name = name
        self.c = c
        self.tQueue = tQueue

    def run(self):



        if self.tQueue.qsize() > 0:
            qMsg = self.tQueue.get()



            try:
                self.c.send(qMsg)
            except socket.close()
                break



class ClientDialog(QDialog):
    ''' An example application for PyQt. Instantiate and call the run method to run. '''
    def __init__(self, threadQueue):

        self.threadQueue = threadQueue

        # create a Qt application --- every PyQt app needs one
        self.qt_app = QApplication(sys.argv)

        # Call the parent constructor on the current object
        QDialog.__init__(self, None)

        # Set up the window
        self.setWindowTitle('IRC Client')
        self.setMaximumSize(500, 200)

        # Add a vertical layaut
        self.vbox = QVBoxLayout()

        # The sender texbox
        self.sender = QLineEdit("", self)

        # The channel region
        self.channal = QTextBrowser()

        # The send button
        self.send_button = GPushButton('&send')

        # Connet the Go button to its callback
        self.send_button.clicked.connect(self.outgoing_parser)

        # Add the controld to the vertical layout
        self.vbox.addWidget(self.channel)
        self.vbox.addWidget(self.sender)
        self.vbox.addWidget(self.send_button)

        # A very stretchy spacer to force the button to the button
        # self.vbox.addStretch(100)
        # Use the vertical layout for the current window
        self.setLayout(self.vbox)

    def cprint(self, data):





        self.channel.append(data)

    def outgoing_parser(self):
        data = self.sender.text()
        if len(data) == 0:
            return
        if data[0] == "/":


            if command == "list":

            elif command == "quit":

            elif command == "msg":

            else:
                self.cprint("Local: Command Error.")
        else:
            self.threadQueue.put("Say " + data)

        self.sender.clear()

        def run(self):
            ''' Run the app and show the main form. '''
            self.show()
            self.qt_app.exec_()


# connect to the server
s = socket.socket()
host =""
port =50000
s.connect((host,port))

sendQueue = Queue.Queue()
app = ClientDialog(sendQueue)

# start threads
rt = ReadThread("ReadThread", s, sendQueue, app)
rt.start()
wt = WriteThread("WriteThread", s, sendQueue)
wt.start()

app.run()

rt.join()
wt.join()
s.close()


