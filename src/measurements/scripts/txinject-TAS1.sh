#!/bin/bash

source config.conf
echo "configure txinjection"
ssh user@node0 'sudo tc qdisc del dev enp5s0 root'
ssh user@node1 'sudo tc qdisc del dev enp5s0 root'
ssh user@node2 'sudo tc qdisc del dev enp5s0 root'
ssh user@node1 'sudo tc qdisc add dev enp5s0 parent root handle 100 taprio \
num_tc 2 \
map 0 0 1 1 0 0 0 0 0 0 0 0 0 0 0 0 \
queues 1@0 1@1 \
base-time 1500 \
sched-entry S 01 16500 \
sched-entry S ff 30500 \
clockid CLOCK_REALTIME'
# open from 16.5us to 30.5us

# video is ID 2, audio is ID 3
ssh user@node2 'sudo tc qdisc add dev enp5s0 parent root handle 100 taprio \
num_tc 2 \
map 0 0 1 1 0 0 0 0 0 0 0 0 0 0 0 0 \
queues 1@0 1@1 \
base-time 1500 \
sched-entry S 01 30500 \
sched-entry S ff 16500 \
clockid CLOCK_REALTIME'