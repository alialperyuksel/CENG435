from socket import *
import sys
import os
import math
import time
import pickle
from datetime import datetime

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

dest_addr = '10.10.2.1'
dest_port = 12002
dest = (dest_addr, dest_port)
listen_addr = '10.10.3.2'
listen_port = 12001
listen = (listen_addr, listen_port)

send_sock = socket(AF_INET, SOCK_DGRAM)
recv_sock = socket(AF_INET, SOCK_DGRAM)

recv_sock.bind(listen)
recv_sock.settimeout(0.1)

print "Ready to serve"

#initializes packet variables 
expectedseqnum=1
ACK=1
ack = []

#RECEIVES DATA
f = open("output.txt", "wb")
endoffile = False
lastpktreceived = time.time()	
starttime = time.time()

while True:

	try:
		rcvpkt=[]
		packet,clientAddress= recv_sock.recvfrom(4096)
		rcvpkt = pickle.loads(packet)
#		check value of checksum received (c) against checksum calculated (h) - NOT CORRUPT
		data = rcvpkt[1]
		checksum = rcvpkt[2]
		if checksum == ip_checksum(data):
#		check value of expected seq number against seq number received - IN ORDER 
			if(rcvpkt[0]==expectedseqnum):
				print "Received inorder", expectedseqnum
				expectedseqnum = expectedseqnum + 1
#				create ACK (seqnum,checksum)
				sndpkt = []
				sndpkt.append(expectedseqnum)
				sndpkt.append(ip_checksum(str(expectedseqnum)))
				pck_to_send = pickle.dumps(sndpkt)

				send_sock.sendto(pck_to_send, dest)
				print "New Ack", expectedseqnum
				if rcvpkt[1]:
					f.write(rcvpkt[1])
				else:
					endoffile = True				

			else:
#		default? discard packet and resend ACK for most recently received inorder pkt
				print "Received out of order", rcvpkt[0]
				sndpkt = []
				sndpkt.append(expectedseqnum)
				sndpkt.append(ip_checksum(str(expectedseqnum)))
				pck_to_send = pickle.dumps(sndpkt)

				send_sock.sendto(pck_to_send, dest)
				print "Ack", expectedseqnum
		else:
			print "checksum error detected"
	except:
		if endoffile:
			if(time.time()-lastpktreceived>3):
				break


endtime = time.time()

f.close()
print 'FILE TRANFER SUCCESSFUL'
print "TIME TAKEN " , str(endtime - starttime)
print datetime.now()

