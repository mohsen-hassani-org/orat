#! /usr/bin/python3
import socket
import traceback
import os
host = ''
port = 10100

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind((host,port))
while 1:
    try:
        message, address = s.recvfrom(10100)
        print ("Got data from", address)
        print ("Message:", message.decode('utf-8'))
        ad = str(address).split("'")
        print(ad[0])
        print(ad[1])
        print(ad[2])
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        traceback.print_exc()
