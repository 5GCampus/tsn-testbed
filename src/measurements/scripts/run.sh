#!/bin/bash

source config.conf
streamconfig="$(echo ${stream1}|cut -d '.' -f1)-$(echo ${stream2}|cut -d '.' -f1)-$(echo ${stream3}|cut -d '.' -f1)"
echo "STARTING TCPDUMP ON NODE0"

timeout 13m ssh -t user@node0 ". /etc/profile && sudo timeout 13m tcpdump ether src 00:00:00:00:00:01 or ether src 00:00:00:00:00:02 or ether src 00:00:00:00:00:03 -i 100 -i enp5s0 -j adapter_unsynced --time-stamp-precision=nano -w ${device}_${streamconfig}_${qos}_${background_size}_${background_traffic}percent.pcap -s 250 "&

echo "START BACKGROUND TRAFFIC (MOONGEN) IN 5s"

sleep 5

timeout 15m ssh  user@node4 "timeout -k 5 13m sudo /home/user/git/MoonGen/build/MoonGen /home/user/git/MoonGen/measurement-2.lua -p ${background_size} -r ${background_traffic} >moongen.log" &

sleep 10

[[ "NULL" != "$stream1" ]] && timeout 13m ssh -t user@node1 'sudo tcpreplay  --loop=1 -i enp1s0 --timer=nano -K --sockprio=2 stream.pcap > replay_node1.log' &
[[ "NULL" != "$stream2" ]] && timeout 13m ssh -t user@node2 'sudo tcpreplay  --loop=1 -i enp1s0 --timer=nano -K --sockprio=2 stream.pcap > replay_node2.log' &
[[ "NULL" != "$stream3" ]] && timeout 13m ssh -t user@node3 'sudo tcpreplay  --loop=1 -i enp1s0 --timer=nano -K --sockprio=2 stream.pcap > replay_node3.log' &

echo "WAIT FOR CAPTURE FINISH"
wait
timeout -k 5 20s ssh  user@node4 "timeout -k 5 10s sudo killall MoonGen"
echo "DONE"
