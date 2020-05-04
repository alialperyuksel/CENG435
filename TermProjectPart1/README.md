Group_no: 25
Name: Yunus Emre GURSES, Ali Alper YUKSEL
ID: 2099083, 2036390

#Requirements
Python
Pip
Ntplib


#Installation
sudo apt update
sudo apt install python-pip
pip install ntplib

Installing these to only source and destination node will be enough.


#TO RUN:
There is one python script for each node. 
Run the python scripts in the following orders: broker.py, r1.py, r2.py, dest.py, source.py
It will send the 10 time data of sending time to the broker. After the data reaches the destination, it, again, fetches data from NTP in destination and calculates the difference and prints in the destination node.

Note: Our implementation sends data not only r1 but also r2. It switches between these nodes. For example: If 10 data is sent from the broker, five of them will be sent through r1 and other 5 will be sent through r2.


#Sync nodes
Ntplib library is used to synchronize the nodes. The time data is fetched from Google servers. There's no need to do anything extra. Script handles.


#Tc/Netem commands

####First, you need to add the 1ms delay. 
To add the delay in broker node, run following commads:

sudo tc qdisc add dev eth1 root netem delay 1ms 5ms distribution normal
sudo tc qdisc add dev eth2 root netem delay 1ms 5ms distribution normal

run the following command for each r1 and r2 node:

sudo tc qdisc add dev eth2 root netem delay 1ms 5ms distribution normal

####Then, changing the delay amount will be enough. Adding 20ms+-5ms delay:

Command in broker node: 
sudo tc qdisc change dev eth1 root netem delay 20ms 5ms distribution normal
sudo tc qdisc change dev eth2 root netem delay 20ms 5ms distribution normal

Command in broker r1 node:
sudo tc qdisc change dev eth2 root netem delay 20ms 5ms distribution normal

Command in broker r2 node: 
sudo tc qdisc change dev eth2 root netem delay 20ms 5ms distribution normal

####Then, changing the delay amount will be enough. Adding 60ms+-5ms delay:

Command in broker node: 
sudo tc qdisc change dev eth1 root netem delay 60ms 5ms distribution normal
sudo tc qdisc change dev eth2 root netem delay 60ms 5ms distribution normal

Command in broker r1 node:
sudo tc qdisc change dev eth2 root netem delay 60ms 5ms distribution normal

Command in broker r2 node: 
sudo tc qdisc change dev eth2 root netem delay 60ms 5ms distribution normal


####To remove the delay:

sudo tc qdisc del dev eth2 root