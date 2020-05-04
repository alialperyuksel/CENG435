import socket

UDP_IP = "10.10.2.2"
UDP_PORT = 12001

sock = socket.socket(socket.AF_INET, #opening a socket to send the data
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT)) #associate the socket with a specific network interface and port number


UDP_IP_2 = "10.10.5.2"
UDP_PORT_2 = 12010 #destination port number

sock_2 = socket.socket(socket.AF_INET, #opening a new socket to send the data to the dest
                     socket.SOCK_DGRAM) # UDP

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes, receive the data
    print "received message:", data
    if(data):
        sock_2.sendto(data, (UDP_IP_2, UDP_PORT_2)) #send the data by using UDP