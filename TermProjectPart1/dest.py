import socket
import ntplib
from datetime import datetime

UDP_IP = "10.10.5.2"
UDP_PORT = 12010

sock = socket.socket(socket.AF_INET, #opening a socket to receive the data
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT)) #associate the socket with a specific network interface and port number

curtime = ntplib.NTPClient()  #object for ntplib

while True:


    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes, receive the data from r1 or r2
    #print "received message:", data
    if(data):
        response = curtime.request('time.google.com') #request the time from NTP 
        dest_time = datetime.fromtimestamp(response.orig_time) #convert to the datetime type
        print "dest time: ", dest_time
        source_time = datetime.strptime(data, '%Y %m %d %H:%M:%S.%f') #convert the source time coming from source to the datetime type
        print "source time: ", source_time
        delay = dest_time - source_time #delay between destination and source
        print(str(delay))