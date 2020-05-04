import socket
import ntplib
from datetime import datetime


TCP_IP = '10.10.1.2'
TCP_PORT = 12000    #defining the TCP port
BUFFER_SIZE = 1024  #buffer size is 1024 bytes


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #opening a socket to send the data
s.connect((TCP_IP, TCP_PORT)) #establish a connection
curtime = ntplib.NTPClient()


for i in range(1,11):
    response = curtime.request('time.google.com')   #request the time from NTP   
    t = datetime.fromtimestamp(response.orig_time)  #convert to the datetime type
    MESSAGE = t.strftime("%Y %m %d %H:%M:%S.%f")    #convert it to the string type 
    s.send(MESSAGE)  #send the message to the socket

s.close()  #close the socket