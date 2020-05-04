Group_no: 25
Name: Yunus Emre GURSES, Ali Alper YUKSEL
ID: 2099083, 2036390

# TO RUN
Run the python scripts in the following orders: broker.py, dest.py, source.py

# Send input.txt file to the source

scp -P 27574 /path/to/file e2099083@pc1.lan.sdn.uky.edu:~

# Used 'datetime' library to calculate difference time

# Routing

sudo route add -host 10.10.2.1 gw 10.10.2.2
sudo route add -host 10.10.3.2 gw 10.10.3.1

# loss
## broker
sudo tc qdisc change dev eth3 root netem loss 0.5% corrupt 0% duplicate 0% delay 3 reorder 0% 0%
## r1
sudo tc qdisc change dev eth1 root netem loss 0.5% corrupt 0% duplicate 0% delay 3 reorder 0% 0%
## dest
sudo tc qdisc change dev eth2 root netem loss 0.5% corrupt 0% duplicate 0% delay 3 reorder 0% 0%

#corruption
## broker
sudo tc qdisc change dev eth3 root netem loss 0% corrupt 0.2% duplicate 0% delay 3 reorder 0% 0%
## r1
sudo tc qdisc change dev eth1 root netem loss 0% corrupt 0.2% duplicate 0% delay 3 reorder 0% 0%
## dest
sudo tc qdisc change dev eth2 root netem loss 0% corrupt 0.2% duplicate 0% delay 3 reorder 0% 0%

#reordering
## broker
sudo tc qdisc change dev eth3 root netem loss 0% corrupt 0% duplicate 0% delay 3 reorder 1% 50%
## r1
sudo tc qdisc change dev eth1 root netem loss 0% corrupt 0% duplicate 0% delay 3 reorder 1% 50%
## dest
sudo tc qdisc change dev eth2 root netem loss 0% corrupt 0% duplicate 0% delay 3 reorder 1% 50%

 