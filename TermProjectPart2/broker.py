from socket import *
import sys
import os
import math
import time
import pickle

TCP_IP = '10.10.1.2'
TCP_PORT = 12000  #defining the TCP port for receiving the data
BUFFER_SIZE = 1024


s = socket(AF_INET, SOCK_STREAM) #opening a socket to receive the daata
s.bind((TCP_IP, TCP_PORT)) #associate the socket with a specific network interface and port number
fileOpen = open('input2.txt','w')
s.listen(1) #enables the broker to accept() connections
while True:
    c, addr = s.accept()     # Establish connection with client.
    print 'Got connection from', addr
    print "Receiving..."
    l = c.recv(BUFFER_SIZE)
    while (l):
        print "Receiving..."
        # print l
        fileOpen.write(l)
        l = c.recv(BUFFER_SIZE)
    print "Done Receiving"
    c.send('Thank you for connecting')
    c.close()
    break 


def ip_checksum(data):  
    pos = len(data)
    if (pos & 1):  # If odd...
        pos -= 1
        sum = ord(data[pos])  # Prime the sum with the odd end byte
    else:
        sum = 0

    #Main code: loop to calculate the checksum
    while pos > 0:
        pos -= 2
        sum += (ord(data[pos + 1]) << 8) + ord(data[pos])

    sum = (sum >> 16) + (sum & 0xffff)
    sum += (sum >> 16)

    result = (~ sum) & 0xffff  # Keep lower 16 bits
    result = result >> 8 | ((result & 0xff) << 8)  # Swap bytes
    return chr(result / 256) + chr(result % 256)  

#port numbers and IPs and create sockets
time.sleep(3)
dest_addr = '10.10.3.2'
dest_port = 12001
dest = (dest_addr, dest_port)
listen_addr = '10.10.2.1'
listen_port = 12002
listen = (listen_addr, listen_port)

#create client socket
send_sock = socket(AF_INET, SOCK_DGRAM)
recv_sock = socket(AF_INET, SOCK_DGRAM)

recv_sock.bind(listen)
recv_sock.settimeout(0.1)

#initializes window variables (upper and lower window bounds, position of next seq number)
base=1
nextSeqnum=1
windowSize=7
window = []

#SENDS DATA
fileOpen= open('input2.txt', 'r') 
data = fileOpen.read(250)
done = False
lastackreceived = time.time()

while not done or window:
#	check if the window is full	or EOF has reached
	if(nextSeqnum<base+windowSize) and not done:
#		create packet(seqnum,data,checksum)
		sndpkt = []
		sndpkt.append(nextSeqnum)
		sndpkt.append(data)
		sndpkt.append(ip_checksum(data))
		pck_to_send = pickle.dumps(sndpkt)
		# print sys.getsizeof(pck_to_send)
#		send packet
		send_sock.sendto(pck_to_send, dest)
		
		print "Sent data", nextSeqnum
#		increment variable nextSeqnum
		nextSeqnum = nextSeqnum + 1
#		check if EOF has reached
		if(not data):
			done = True
#		append packet to window
		window.append(pck_to_send)
#		read more data
		data = fileOpen.read(250)

	# RECEIPT OF AN ACK
	try:
		packet,serverAddress = recv_sock.recvfrom(4096)
		rcvpkt = []
		rcvpkt = pickle.loads(packet)
	#check value of checksum received against checksum calculated 
		seq = rcvpkt[0]
		checksum = str(rcvpkt[1])
		if checksum == ip_checksum(str(seq)):
			print "Received ack for", rcvpkt[0]
	#slide window and reset timer
			while rcvpkt[0]>base and window:
				lastackreceived = time.time()
				del window[0]
				base = base + 1
		else:
			print "error detected"
	#TIMEOUT
	except:
		if(time.time()-lastackreceived>0.01):
			for i in window:
				send_sock.sendto(i, dest)

fileOpen.close()

print "connection closed"    
send_sock.close()
