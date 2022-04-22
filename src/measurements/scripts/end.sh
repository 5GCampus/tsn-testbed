#!/bin/bash

source config.conf

scripts/check_ptp.sh
streamconfig="$(echo ${stream1}|cut -d '.' -f1)-$(echo ${stream2}|cut -d '.' -f1)-$(echo ${stream3}|cut -d '.' -f1)"
# check if PTP errors occured while runtime
PTP_start=$(cat ptp.log| grep "START" | cut -d "=" -f2)
ssh user@node0 'sudo journalctl -u ptp4l.service --since "'$PTP_start'" -g "ANNOUNCE_RECEIPT_TIMEOUT_EXPIRES" -q -o json --no-pager' | grep "ANNOUNCE_RECEIPT_TIMEOUT_EXPIRES" && echo "ERROR">>ptp.log
ssh user@node1 'sudo journalctl -u ptp4l.service --since "'$PTP_start'" -g "ANNOUNCE_RECEIPT_TIMEOUT_EXPIRES" -q -o json --no-pager' | grep "ANNOUNCE_RECEIPT_TIMEOUT_EXPIRES" && echo "ERROR">>ptp.log
ssh user@node2 'sudo journalctl -u ptp4l.service --since "'$PTP_start'" -g "ANNOUNCE_RECEIPT_TIMEOUT_EXPIRES" -q -o json --no-pager' | grep "ANNOUNCE_RECEIPT_TIMEOUT_EXPIRES" && echo "ERROR">>ptp.log
ssh user@node3 'sudo journalctl -u ptp4l.service --since "'$PTP_start'" -g "ANNOUNCE_RECEIPT_TIMEOUT_EXPIRES" -q -o json --no-pager' | grep "ANNOUNCE_RECEIPT_TIMEOUT_EXPIRES" && echo "ERROR">>ptp.log

ssh user@node1 'sudo journalctl -u phc2sys.service --since "'$PTP_start'" -q   --no-pager | sed -e "s/[[:space:]]\+/ /g" | cut -d " " -f10' | while read -r line ; do
    if [ "$line" -gt "1000" ]; then
		echo "ERROR">>ptp.log
		fi
		if [ "$line" -lt "-1000" ]; then
		echo "ERROR">>ptp.log
		fi
done
ssh user@node2 'sudo journalctl -u phc2sys.service --since "'$PTP_start'" -q   --no-pager | sed -e "s/[[:space:]]\+/ /g" | cut -d " " -f10' | while read -r line ; do
    if [ "$line" -gt "1000" ]; then
		echo "ERROR">>ptp.log
		fi
		if [ "$line" -lt "-1000" ]; then
		echo "ERROR">>ptp.log
		fi
done
ssh user@node3 'sudo journalctl -u phc2sys.service --since "'$PTP_start'" -q   --no-pager | sed -e "s/[[:space:]]\+/ /g" | cut -d " " -f10' | while read -r line ; do
    if [ "$line" -gt "1000" ]; then
		echo "ERROR">>ptp.log
		fi
		if [ "$line" -lt "-1000" ]; then
		echo "ERROR">>ptp.log
		fi
done

echo "###node4"> moongen.log
ssh user@node4 'cat  moongen.log' >>moongen.log
cat moongen.log
echo "SAVE CAPTURE DATA"
fn=""
cat ptp.log | grep "ERROR" || rsync -avP user@node0:/home/user/${device}_${streamconfig}_${qos}_${background_size}_${background_traffic}percent.pcap /mnt/harddrive/data/pcaps/${device}_${streamconfig}_${qos}_${background_size}_${background_traffic}percent.pcap
cat moongen.log | grep "ERROR" && rm /mnt/harddrive/data/pcaps/${device}_${streamconfig}_${qos}_${background_size}_${background_traffic}percent.pcap && echo "moongen fail, remove pcap"&&fn=""
ssh user@node0 "rm /home/user/${device}_${streamconfig}_${qos}_${background_size}_${background_traffic}percent.pcap"
cat ptp.log | grep "ERROR" || echo "OK" >> ptp.log