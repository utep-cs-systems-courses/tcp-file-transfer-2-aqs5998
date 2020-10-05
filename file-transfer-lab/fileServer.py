#! /usr/bin/env python3

import sys
sys.path.append("../lib")       # for params
import re, socket, params

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

sock, addr = lsock.accept()

print("connection rec'd from", addr)


from framedSock import framedSend, framedReceive

while True:
    payload = framedReceive(sock, debug)
    if debug: print("rec'd: ", payload)
    if not payload:
        break
    simpleVar = payload.decode()
    try: 
        framedSend(sock, payload, debug)
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
        payload = framedReceive(sock, debug)
        output = open(output_file, 'w')
        payload = payload.decode('utf8')
        output.write(payload)
    else:
        payload = framedReceive(sock, debug)
        output = open(output_file, 'w')
        payload = payload.decode('utf8')
        output.write(payload)