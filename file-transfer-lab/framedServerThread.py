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

from threading import Thread, enumerate, Lock 
from encapFramedSock import EncapFramedSock
global dictionary   #Initialize Variables
global l
l = Lock()
dictionary = dict()

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
            #aquire lock
            #Check to see 
            # if file is in dictionary
            if output_file in dictionary:
                #Write to the client failure
                self.fsock.send(b"False", debug)     
                l.release()
                exit
            else:
                dictionary.update(output_file)
                l.release()
            #      release lock
            #      exit
            #Else 
            #       Add to dictionary
            #release lock
            if (output_file):
                payload = self.fsock.receive(debug)
                output = open(output_file, 'wb')
                output.write(payload)
                #self.fsock.send(payload, debug)
            else:
                #Lock aquire to prevent other processes from access 
                payload = self.fsock.receive(debug)
                output = open(output_file, 'wb')
                output.write(payload)
                try:
                    self.fsock.send(payload, debug)
                except:
                    print("connection lost while sending.")
                    print("connection lost while sending.")
                    print("connection lost while sending.")
                output.close()
                #Delete dictionary 
                l.acquire()       
                del dictionary[payload]
                l.release()
                

while True:
    sockAddr = lsock.accept()
    server = Server(sockAddr)
    server.start()