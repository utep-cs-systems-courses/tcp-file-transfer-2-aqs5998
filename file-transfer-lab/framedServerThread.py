#! /usr/bin/env python3

import sys
sys.path.append("../lib")       # for params
import re, socket, params, os

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

from threading import Thread;
from encapFramedSock import EncapFramedSock

class Server(Thread):
    def __init__(self, sockAddr):
        Thread.__init__(self)
        self.sock, self.addr = sockAddr
        self.fsock = EncapFramedSock(sockAddr)
    def run(self):
        print("new thread handling connection from", self.addr)
        while True:
            payload = self.fsock.receive(debug)
            if debug: print("rec'd: ", payload)
            if not payload:     # done
                if debug: print(f"thread connected to {addr} done")
                self.fsock.close()
                return          # exit
            simpleVar = payload.decode()
            try: 
                self.fsock.send(payload, debug)
            except:
                print("Connection was cut short try again")
                inputVar = input("Would you like to continue recieving anyways?: yes/no")
                if inputVar == "yes":
                    continue
                else:
                    print("Now exiting")
                    sys.exit(0)
            output_file = simpleVar
            if (output_file):
                payload = self.fsock.receive(debug)
                output = open(output_file, 'w')
                payload = payload.decode('utf8')
                output.write(payload)
                #self.fsock.send(payload, debug)
            else:
                payload = self.fsock.receive(debug)
                output = open(output_file, 'w')
                payload = payload.decode('utf8')
                output.write(payload)
                self.fsock.send(payload, debug)
                

while True:
    sockAddr = lsock.accept()
    server = Server(sockAddr)
    server.start()