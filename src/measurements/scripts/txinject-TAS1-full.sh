#!/bin/bash

source config.conf
echo "configure txinjection"
ssh user@node1 'sudo tc qdisc del dev enp1s0 root'
ssh user@node2 'sudo tc qdisc del dev enp1s0 root'
ssh user@node3 'sudo tc qdisc del dev enp1s0 root'

ssh user@node1 'sudo tc qdisc replace dev enp1s0 parent root handle 100 taprio \
        num_tc 2 \
        map 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 \
        queues 1@0 1@1 \
        base-time 0 \
        sched-entry S FF 50000 \
        sched-entry S FD 450000 \
      	flags 0x1 \
      	txtime-delay 500000 \
        clockid CLOCK_TAI '     
ssh user@node1 'sudo tc qdisc replace dev enp1s0 parent 100:1 etf \
        clockid CLOCK_TAI \
        delta 500000 \
        offload \
        skip_sock_check'
ssh user@node1 'sudo tc qdisc replace dev enp1s0 parent 100:2 etf \
        clockid CLOCK_TAI \
        delta 500000 \
        offload \
        skip_sock_check'    
ssh user@node2 'sudo tc qdisc replace dev enp1s0 parent root handle 100 taprio \
        num_tc 2 \
        map 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 \
        queues 1@0 1@1 \
        base-time 150000 \
        sched-entry S FF 50000 \
        sched-entry S FD 450000 \
      	flags 0x1 \
      	txtime-delay 500000 \
        clockid CLOCK_TAI '     
ssh user@node2 'sudo tc qdisc replace dev enp1s0 parent 100:1 etf \
        clockid CLOCK_TAI \
        delta 500000 \
        offload \
        skip_sock_check'
ssh user@node2 'sudo tc qdisc replace dev enp1s0 parent 100:2 etf \
        clockid CLOCK_TAI \
        delta 500000 \
        offload \
        skip_sock_check'
ssh user@node3 'sudo tc qdisc replace dev enp1s0 parent root handle 100 taprio \
        num_tc 2 \
        map 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 \
        queues 1@0 1@1 \
        base-time 300000 \
        sched-entry S FF 100000 \
        sched-entry S FD 400000 \
      	flags 0x1 \
      	txtime-delay 500000 \
        clockid CLOCK_TAI '     
ssh user@node3 'sudo tc qdisc replace dev enp1s0 parent 100:1 etf \
        clockid CLOCK_TAI \
        delta 500000 \
        offload \
        skip_sock_check'
ssh user@node3 'sudo tc qdisc replace dev enp1s0 parent 100:2 etf \
        clockid CLOCK_TAI \
        delta 500000 \
        offload \
        skip_sock_check'