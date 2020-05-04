import socket


TCP_IP = '10.10.1.2'
TCP_PORT = 12000  #defining the TCP port for receiving the data
BUFFER_SIZE = 1024  # Normally 1024 buffer size


UDP_IP1 = "10.10.2.2"
UDP_PORT1 = 12001   #defining the UDP port for r1


UDP_IP2 = "10.10.4.2"
UDP_PORT2 = 12004   #defining the UDP port for r2

i = 1

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #opening a socket to receive the daata
s.bind((TCP_IP, TCP_PORT)) #associate the socket with a specific network interface and port number
s.listen(1) #enables the broker to accept() connections

conn, addr = s.accept()
print ('Connection address:', addr)
while 1:
    data = conn.recv(BUFFER_SIZE) #receive the data from source
    if not data: break


    print "UDP target IP:", UDP_IP1
    print "UDP target port:", UDP_PORT1
    print "message:", data

    sock = socket.socket(socket.AF_INET, #opening a new socket to send the data to the r1 or r2, switching between r1 and r2 while sending the data
                             socket.SOCK_DGRAM) # UDP
    if i == 1:
        sock.sendto(data, (UDP_IP1, UDP_PORT1)) #send the data to r1
    if i == 2:
        sock.sendto(data, (UDP_IP2, UDP_PORT2)) #send the data to r2
    i = i+1
    if i == 3:
        i = 1
conn.close() #close the connection