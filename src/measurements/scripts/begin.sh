#!/bin/bash

source config.conf

echo "CONFIGURE QDISC..."

# mapping socket-prio=1(ptp) to hw queue 0, everything elso to queue 1

ssh user@node0 'sudo tc qdisc del dev enp5s0 root'
ssh user@node1 'sudo tc qdisc del dev enp1s0 root'
ssh user@node2 'sudo tc qdisc del dev enp1s0 root'
ssh user@node3 'sudo tc qdisc del dev enp1s0 root'

ssh user@node0 'sudo killall -9 tcpdump'
ssh user@node1 'sudo killall -9 tcpreplay'
ssh user@node2 'sudo killall -9 tcpreplay'
ssh user@node3 'sudo killall -9 tcpreplay'

ssh user@node1 'rm -r /home/user/stream.pcap'
ssh user@node2 'rm -r /home/user/stream.pcap'
ssh user@node3 'rm -r /home/user/stream.pcap'

ssh user@node0 'sudo systemctl start ptp4l.service'
ssh user@node1 'sudo systemctl start ptp4l.service'
ssh user@node2 'sudo systemctl start ptp4l.service'
ssh user@node3 'sudo systemctl start ptp4l.service'

ssh user@node0 'sudo ethtool -L enp5s0 combined 2 && sudo tc qdisc add dev enp5s0 parent root handle 6666 mqprio num_tc 2 map 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1  queues 1@0 1@1 hw 0'&
ssh user@node1 'sudo ethtool -L enp1s0 combined 4 && sudo tc qdisc add dev enp1s0 parent root handle 6666 mqprio num_tc 2 map 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1  queues 1@0 1@1 hw 0'&
ssh user@node2 'sudo ethtool -L enp1s0 combined 4 && sudo tc qdisc add dev enp1s0 parent root handle 6666 mqprio num_tc 2 map 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1  queues 1@0 1@1 hw 0'&
ssh user@node3 'sudo ethtool -L enp1s0 combined 4 && sudo tc qdisc add dev enp1s0 parent root handle 6666 mqprio num_tc 2 map 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1  queues 1@0 1@1 hw 0'&

wait
ssh user@node0 'tc qdisc show | grep mqprio'
ssh user@node1 'tc qdisc show | grep mqprio'
ssh user@node2 'tc qdisc show | grep mqprio'
ssh user@node3 'tc qdisc show | grep mqprio'

if [ $device = "InnoRoute-TrustNode" ]; then
    scripts/trustnode.sh
fi
echo $qos | grep "txinject" && scripts/$qos.sh  #configure tas on node1/2

ssh user@node1 'tc qdisc show '
ssh user@node2 'tc qdisc show '
ssh user@node3 'tc qdisc show '
# wait for ptp resync
sleep 30 

echo "SYNC TEST DATA"
echo -e "\t Stream1=$stream1"
echo -e "\t Stream2=$stream2"
echo -e "\t Stream3=$stream3\n"
[[ "NULL" != "$stream1" ]] && rsync -L -a ../pcap_writer/$stream1 user@node1:/home/user/stream.pcap
[[ "NULL" != "$stream2" ]] && rsync -L -a ../pcap_writer/$stream2 user@node2:/home/user/stream.pcap
[[ "NULL" != "$stream3" ]] && rsync -L -a ../pcap_writer/$stream3 user@node3:/home/user/stream.pcap

echo "CONFIGURE INTERFACES ON BACKGROUND DEVICES"
timeout -k 5 20s ssh  user@node4 "timeout -k 5 10s sudo killall MoonGen"
ssh user@node4 'sudo /home/user/git/MoonGen/prestart-2.sh'

echo "PTP" > ptp.log
echo "START=$(date '+%F %T')" >> ptp.log
echo "START=$(date '+%F %T')"

scripts/check_ptp.sh
