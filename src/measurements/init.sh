#!/bin/bash

eval `ssh-agent -s`
ssh-add _your_ssh_key_
source config.conf

ssh user@node1 'sudo ip link set INTERFACE up'
ssh user@node2 'sudo ip link set INTERFACE up'
ssh user@node3 'sudo ip link set INTERFACE up'
ssh user@node1 'sudo tc qdisc del dev INTERFACE root'
ssh user@node2 'sudo tc qdisc del dev INTERFACE root'
ssh user@node3 'sudo tc qdisc del dev INTERFACE root'
sleep 30

sizes=(64 1518)
traffic=(0 85 100 150 200)

# PCAP files correspond to the paper
streamsets=(\
'streamset=("robotic.pcap" "NULL" "NULL")' \
'streamset=("audioBBB.pcap" "NULL" "NULL")' \
'streamset=("videoBBB.pcap" "NULL" "NULL")' \
'streamset=("podcast.pcap" "NULL" "NULL")' \
'streamset=("spotJPEGspot.pcap" "NULL" "NULL")' \
'streamset=("spotWASDspot.pcap" "NULL" "NULL")' \
'streamset=("spotWASDspot.pcap" "podcast.pcap" "spotJPEGspot.pcap")' \
'streamset=("robotic.pcap" "audioBBB.pcap" "videoBBB.pcap")' \
)

for streams in "${streamsets[@]}"; do
	eval $streams
	stream1=${streamset[0]}
	stream2=${streamset[1]}
	stream3=${streamset[2]}
	for s in "${sizes[@]}"; do
		for t in "${traffic[@]}"; do
			start=$(date +'%s')
			echo "START AT $(date "+%FT%T" | sed 's/:/-/g')"
			echo "SIZE: ${s} TRAFFIC: ${t} %"
			./update_config.py -bs=${s} -bt=${t} --s1=${stream1} --s2=${stream2} --s3=${stream3}
			scripts/measure.sh
			end=$(date +'%s')
			let duration=end-start
			echo "FINISHED in ${duration}s"
			echo "FINISHED AT $(date "+%FT%T" | sed 's/:/-/g')"
			echo "COOL DOWN 5 sec"
			sleep 5
		done
	done
done
killall ssh-agent
