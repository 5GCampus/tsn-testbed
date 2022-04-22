#!/bin/bash

source config.conf

n=0
x=0
y=0

echo "RUN MEASUREMENT"

# test at most 10x with same configuration
until [ "$x" -ge 10 ]
do
	until [ "$n" -ge 10 ]
	do
		scripts/begin.sh
		scripts/run.sh
		scripts/end.sh
		n=$((n+1))
		cat ptp.log | grep "OK" || echo "measured rubish because of PTP error, run again..."
		cat ptp.log | grep "OK" && break
		timeout -k 5 20s ssh user@node4 "timeout -k 5 10s sudo killall MoonGen"
		ssh user@node1 'sudo tc qdisc del dev enp1s0 root'
		ssh user@node2 'sudo tc qdisc del dev enp1s0 root'
		ssh user@node3 'sudo tc qdisc del dev enp1s0 root'
		sleep 60
	done
	x=$((x+1))
	cat moongen.log | grep "Found 0 usable devices" || break
	echo "error: rebooting moongen nodes"
	timeout 1m ssh user@node4 'sudo reboot' &
	wait
	y=0
	until [ "$y" -ge 10 ]
	do
		y=$((y+1))
		ping -c3 node4 && break
		sleep 60
	done
	sleep 30
done
