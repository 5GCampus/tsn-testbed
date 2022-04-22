#!/bin/env python3

from argparse import ArgumentParser
from fileinput import input

parser = ArgumentParser()
parser.add_argument("-bs", "--background_size",
                    help="background frame size in bytes",
                    required=True,
                    type=int)
parser.add_argument("-bd", "--background_delay",
                    help="background inter frame gap in nano seconds",
                    required=False,
                    type=int)
parser.add_argument("-bt", "--background_traffic",
                    help="background traffic in Mpps",
                    required=True,
                    type=float)
parser.add_argument("-dev", "--device",
                    help="device name",
                    required=False,
                    type=str)   
parser.add_argument("-qos", "--qos",
                    help="qos",
                    required=False,
                    type=str)
parser.add_argument("-s1", "--s1",
                    help="stream1",
                    required=False,
                    type=str,
                    default="")     
parser.add_argument("-s2", "--s2",
                    help="stream2",
                    required=False,
                    type=str,
                    default="")
parser.add_argument("-s3", "--s3",
                    help="stream3",
                    required=False,
                    type=str,
                    default="")               
parser.add_argument("-f", "--file",
                    help="config file",
                    required=False,
                    type=str,
                    default="config.conf")
args = parser.parse_args()

for line in input(args.file, inplace=True):
    if "background_size" in line:
        line = "background_size={}\n".format(args.background_size)
        print(line, end="")
    elif "background_traffic" in line:
        line = "background_traffic={}\n".format(args.background_traffic)
        print(line, end="")
    elif "device" in line:
        if args.device:
        	line = 'device="{}"\n'.format(args.device)
        print(line, end="")
    elif "qos" in line:
        if args.qos:
        	line = 'qos="{}"\n'.format(args.qos)
        print(line, end="")
    elif "stream1" in line:
        if args.s1:
        	line = 'stream1="{}"\n'.format(args.s1)
        print(line, end="")
    elif "stream2" in line:
        if args.s2:
        	line = 'stream2="{}"\n'.format(args.s2)
        print(line, end="")
    elif "stream3" in line:
        if args.s3:
        	line = 'stream3="{}"\n'.format(args.s3)
        print(line, end="")
    elif "background_delay" in line:
        if args.background_delay:
            line = "background_delay={}n\n".format(args.background_delay)
        print(line, end="")
    else:
        print(line, end="")
