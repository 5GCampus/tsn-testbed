#!/bin/bash
#TSN switch specific configuration
source config.conf
echo "remove old rules from TrustNode (TN)"
ssh root@trustnode 'TNflowtable del -U0 -O0 -q0'
ssh root@trustnode 'TNflowtable del -U1 -O0 -q0'
ssh root@trustnode 'TNflowtable del -U2 -O0 -q0'
ssh root@trustnode 'TNflowtable del -U3 -O0 -q0'
ssh root@trustnode 'TNflowtable del -U4 -O0 -q0'
ssh root@trustnode 'TNflowtable del -U5 -O0 -q0'
ssh root@trustnode 'TNflowtable del -U6 -O0 -q0'
ssh root@trustnode 'TNflowtable del -U7 -O0 -q0'
ssh root@trustnode 'TNflowtable del -U0 -O0 -q0'
ssh root@trustnode 'TNflowtable del -U1 -O0 -q1'
ssh root@trustnode 'TNflowtable del -U2 -O0 -q2'
ssh root@trustnode 'TNflowtable del -U3 -O0 -q3'
ssh root@trustnode 'TNflowtable del -U4 -O0 -q4'
ssh root@trustnode 'TNflowtable del -U5 -O0 -q5'
ssh root@trustnode 'TNflowtable del -U6 -O0 -q6'
ssh root@trustnode 'TNflowtable del -U7 -O0 -q7'  

ssh root@trustnode 'TNtsnctl config_change -P0 -g0' # tas off

echo "set new rules to TN"

if [ $qos = "No-QoS" ]; then
	ssh root@trustnode 'TNflowtable add -U0 -O0 -q0'
	ssh root@trustnode 'TNflowtable add -U1 -O0 -q0'
	ssh root@trustnode 'TNflowtable add -U2 -O0 -q0'
	ssh root@trustnode 'TNflowtable add -U3 -O0 -q0'
	ssh root@trustnode 'TNflowtable add -U4 -O0 -q0'
	ssh root@trustnode 'TNflowtable add -U5 -O0 -q0'
	ssh root@trustnode 'TNflowtable add -U6 -O0 -q0'
	ssh root@trustnode 'TNflowtable add -U7 -O0 -q0'   
fi
if [ $qos = "IEEE-802.1p" ]; then
	ssh root@trustnode 'TNflowtable add -U0 -O0 -q0'
	ssh root@trustnode 'TNflowtable add -U1 -O0 -q1'
	ssh root@trustnode 'TNflowtable add -U2 -O0 -q2'
	ssh root@trustnode 'TNflowtable add -U3 -O0 -q3'
	ssh root@trustnode 'TNflowtable add -U4 -O0 -q4'
	ssh root@trustnode 'TNflowtable add -U5 -O0 -q5'
	ssh root@trustnode 'TNflowtable add -U6 -O0 -q6'
	ssh root@trustnode 'TNflowtable add -U7 -O0 -q7'   
fi
if [ $qos = "IEEE-802.1p-R" ]; then
	ssh root@trustnode 'TNflowtable add -U0 -O0 -q7'
	ssh root@trustnode 'TNflowtable add -U1 -O0 -q6'
	ssh root@trustnode 'TNflowtable add -U2 -O0 -q5'
	ssh root@trustnode 'TNflowtable add -U3 -O0 -q4'
	ssh root@trustnode 'TNflowtable add -U4 -O0 -q3'
	ssh root@trustnode 'TNflowtable add -U5 -O0 -q2'
	ssh root@trustnode 'TNflowtable add -U6 -O0 -q1'
	ssh root@trustnode 'TNflowtable add -U7 -O0 -q0'   
fi
