#!/usr/bin/env python

import socket
import time
from datetime import datetime


TCP_IP = '10.10.1.2'
TCP_PORT = 12000    #defining the TCP port
BUFFER_SIZE = 1024  #buffer size is 1024 bytes

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #opening a socket to send the data
s.connect((TCP_IP, TCP_PORT)) #establish a connection

f = open('input.txt','rb')
print 'Sending...'

l = f.read(1024)
start = datetime.now()
while (l):
    print 'Sending...'
    s.send(l)
    l = f.read(1024)
f.close()
print "Done Sending" 
s.shutdown(socket.SHUT_WR)
print s.recv(1024)
print start
s.close()  #close the socket

