#! /usr/bin/python3
import socket
import sys
import traceback
#print socket.gethostname()
#print socket.gethostbyname(socket.gethostname())
#print socket.gethostbyaddr(socket.gethostbyname(socket.gethostname()))
msg = socket.gethostbyname(socket.gethostname())
msg_bytes = bytes(msg, 'utf-8')
dest = ('<broadcast>',10100)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.sendto(msg_bytes, dest)
print ("Looking for replies; press Ctrl-C to stop.")
while 1:
    (buf,address)=s.recvfrom(10100)
    if not len(buf):
        break
    print("received from %s: %s" %(address, buf))