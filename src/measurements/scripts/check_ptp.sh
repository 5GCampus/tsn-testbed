#!/bin/bash

echo "node0 ptp status"
ssh user@node0 'sudo pmc -u -b 0 "get CURRENT_DATA_SET" -f ptp/ptp3.conf' | grep offsetFromMaster
ssh user@node0 'sudo pmc -u -b 0 "GET PORT_DATA_SET" -f ptp/ptp3.conf' | grep portState | grep SLAVE || echo "ERROR" >> ptp.log 

echo "node1 ptp status"
ssh user@node1 'sudo pmc -u -b 0 "get CURRENT_DATA_SET" -f ptp/ptp3.conf' | grep offsetFromMaster
ssh user@node1 'sudo pmc -u -b 0 "GET PORT_DATA_SET" -f ptp/ptp3.conf' | grep portState | grep SLAVE || echo "ERROR" >> ptp.log 

echo "node2 ptp status"
ssh user@node2 'sudo pmc -u -b 0 "get CURRENT_DATA_SET" -f ptp/ptp3.conf' | grep offsetFromMaster
ssh user@node2 'sudo pmc -u -b 0 "GET PORT_DATA_SET" -f ptp/ptp3.conf' | grep portState | grep SLAVE || echo "ERROR" >> ptp.log 

echo "node3 ptp status"
ssh user@node3 'sudo pmc -u -b 0 "get CURRENT_DATA_SET" -f ptp/ptp3.conf' | grep offsetFromMaster
ssh user@node3 'sudo pmc -u -b 0 "GET PORT_DATA_SET" -f ptp/ptp3.conf' | grep portState | grep SLAVE || echo "ERROR" >> ptp.log