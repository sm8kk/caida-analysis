# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 13:10:26 2016

@author: souravmaji
"""

from __future__ import division
import sys
import numpy as np
#f = open("packets-10k.txt", 'r')
f = open(str(sys.argv[1]), 'r')

lines = f.readlines()

# Close the file
f.close()


delta = 1e-6
burstCount = 1
pktsBurst = 0
burstSize = 0
flowID = {}
firstTime = 1
cumPktCount = 0

print "cumPktCount,burstNum,burstSize,pktsBurst,pktsFlow,maxBytesFlow,fractionFlowBytes"
for l in lines:  # For every line in the file
    val = l.split(",")  # Create a tuple (immutable list) from the fields
    #first group the packets in a burst, and within the burst find the flowID with max packets
    #for grouping into burst lets say 3 packets arrive as (p1,p2,p3)
    #if ts(p2) ~ ts(p1) + length(p1)/NIC rate then p1 and p2 are in the same burst
    ts = float(val[1])
    srcIP = val[2]
    dstIP = val[3]
    prot = val[7]
    srcPort = val[4]
    dstPort = val[5]
    
    key = srcIP + "-" + dstIP + "-" + prot + "-" + srcPort + "-" + dstPort    
    pktLen = int(val[6])
    
    if (firstTime == 1):
        ts_prev = ts
        len_prev = pktLen
        firstTime = 0
        pktsBurst = 1
        burstSize = len_prev
	cumPktCount = 1
        # add an entry to the dictionary of flowID's
        # the data structure keeps track of a flows number of packets and bytes
        flowID[key] = [1]
        flowID[key].append(len_prev)
        continue;
            
    ts_now = ts
    #print ts_now
    #print (ts_prev + len_prev*8/(1e10))
    if((ts_now - (ts_prev + len_prev*8/(1e10))) < delta):
        # the new packet is in the same burst
	cumPktCount = cumPktCount + 1
        pktsBurst = pktsBurst + 1
        burstSize = burstSize + pktLen
        ts_prev = ts
        len_prev = pktLen
        
        if key in flowID.keys():
            flowID[key][0] = flowID[key][0] + 1
            flowID[key][1] = flowID[key][1] + pktLen
        else:
            flowID[key] = [1]
            flowID[key].append(pktLen)
    else:
        #find the flow with the max number of bytes
        k = flowID.items()[0][0]
        mx_bytes = flowID[k][1]
        mx_k = k
        for k in flowID.keys():
            if(flowID[k][1] > mx_bytes):
                mx_bytes = flowID[k][1]
                mx_k = k
        
        maxBytesPkt = flowID[mx_k][0]        
        #print burst details
        op = str(cumPktCount) + "," + str(burstCount) + "," + str(burstSize) + "," + str(pktsBurst) + "," +\
        str(maxBytesPkt) + "," + str(mx_bytes) + "," + str(mx_bytes/burstSize)
        print op
        #print("\n")
        cumPktCount = cumPktCount + 1
        burstCount = burstCount + 1
        pktsBurst = 1
        burstSize = pktLen
        ts_prev = ts_now
        flowID = {}
        flowID[key] = [1]
        flowID[key].append(pktLen)
        
