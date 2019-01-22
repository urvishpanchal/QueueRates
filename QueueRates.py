#!/usr/bin/env python
# Copyright (c) 2019 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.
# 01/21/2019 by urvish@arista.com

import PyClient,argparse
import json
import time
from collections import defaultdict

def parse_args():
    parser = argparse.ArgumentParser(epilog="Example: python QueueRates.py -e Ethernet29 -l 30")
    parser.add_argument("-l", "--loadInterval", type=int, default=10, help="Specify load interval time in seconds")
    parser.add_argument("-e", "--ethernet", nargs='+', default=["Ethernet1/1"], help="Ethernet Interface List")
    args = parser.parse_args()
    return args

def getQueueByteCount(ethernet, loadInterval):
    import requests
    response1 = requests.get('http://localhost:6060/rest/Smash/counters/queue/SandCounters/current/intfQueueCounter')
    time.sleep(loadInterval)
    response2 = requests.get('http://localhost:6060/rest/Smash/counters/queue/SandCounters/current/intfQueueCounter')
    for interface,value in json.loads(response1.content).iteritems():
        if ethernet in interface:
            for stats,queue in value.iteritems():
                if "intfQueueStat" in stats:
                    firstReading = queue
    for interface,value in json.loads(response2.content).iteritems():
        if ethernet in interface:
            for stats,queue in value.iteritems():
                if "intfQueueStat" in stats:
                    secondReading = queue
    return(firstReading, secondReading)


def calculateDiff(firstReading, secondReading, loadInterval):
    diff = defaultdict(dict)
    for first,second in zip(firstReading,secondReading):
        if first['queueType'] == "uc":
            for k in first:
                if isinstance(first[k],(int,long)):
                    diff[firstReading.index(first)][k] = float(second[k]-first[k])/loadInterval
    return diff


def renderOutput(diff):
    counterDisplayFormat = "%-20s %18s %15s %15s %15s"
    print counterDisplayFormat % ( "Queue", "Mbps",
                                              "Pkts/s",
                                              "BitsDropped/s",
                                              "PktsDropped/s")
    for queue, data in diff.iteritems():
        print counterDisplayFormat % ( queue, data['bytes']/125000,
                                              data['pkts'],
                                              data['bytesDropped']/125000,
                                              data['pktsDropped'])

def main():
    args = parse_args()
    try:
        for eth in args.ethernet:
            firstReading, secondReading = getQueueByteCount(eth, args.loadInterval)
            diff = calculateDiff(firstReading, secondReading, args.loadInterval) 
            renderOutput(diff)
    except:
        print("Have you enabled Terminattr?")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
