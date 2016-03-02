# -*- coding: utf-8 -*-
from __future__ import division
import sys
import numpy as np
"""
Created on Thu Jan  7 13:10:26 2016
Modified by Austin in January and February
Last modified on Feb 10th
@author: Sourav, Austin, Sherry
"""

"""
Clarification:

Data used by Sourav is in the format:
4,187.119.42.166,32.193.93.47,80,24381,1444,00.000009537


The meaning of each part follow:
packetId, srcIp, desIp, srcPort, desPort, length,time, time


Austin
"""

"""
Method Improvement:

In the program, we used much more accurate time data for analysis.
The code works for packets whose timestamps are in ns. We have a good degree
of confidence to say that there is no overlap between the packets (which is
theoritically true), but we notice the same thing given the inaccuracies inherent
in the timestamping process.

We chose a delta of 10ns, since  64B packet over a 10 Gbps link has a transmission
time of 51 ns. So we keep a gap of 10ns which is 20% of the minimum packet
transmission time.


Jan 10th
Austin
"""


f = open("simpleData.txt", 'r')
lines = f.readlines()
f.close()

f = open('burstInMinute1.txt', 'w')


delta = 1e-8 # 10 ns as the delta
linkRate = float(10000000000)
# Those two are constants

packetId = 1
# the Id of the packet.

burstId = 1
# To count the number of burst

pktsInBurst = 0
# To count the number of packets in a burst

burstLastPacketId = 0
# To identify the last packet in the burst

burstBeginTime = 0
# To record the beginning time of a burst

flowID = {}

firstTime = 1
len_prev = 0
ts_prev = 0
ts_now = 0

burstSize = 0
# The size of a burst, in bytes


f.write( "burstLastPacketId,burstId,burstSize,pktsInBurst,pktsFlow,maxBytesFlow,fractionFlowBytes")
f.write("\n")

for l in lines:  # For every line in the file
    val = l.split(",")  # Create a tuple (immutable list) from the fields
    #first group the packets in a burst, and within the burst find the flowID with max packets
    #for grouping into burst lets say 3 packets arrive as (p1,p2,p3)
    #if ts(p2) ~ ts(p1) + length(p1)/NIC rate then p1 and p2 are in the same burst
    packetId = int(val[0])
    ts = float(val[6])
    srcIP = val[1]
    dstIP = val[2]
    srcPort = val[3]
    dstPort = val[4]
    pktLen = float(val[5])
    
    key = srcIP + "-" + dstIP + "-" + srcPort + "-" + dstPort    
    
    if (firstTime == 1):
        ts_now = ts
        len_prev = pktLen
        firstTime = 0
        pktsInBurst = 1
        burstSize = len_prev
	burstLastPacketId = packetId
        ts_prev = ts
        # add an entry to the dictionary of flowID's
        # the data structure keeps track of a flows number of packets and bytes
        flowID[key] = [1]
        flowID[key].append(len_prev)
        burstBeginTime = ts_now
        continue;
            
    ts_now = ts
    #print ts_now
    #print (ts_prev + len_prev*8/(1e10))
    if (ts_now - (ts_prev + len_prev*8/linkRate) < delta):
        # then the  new packet is in the same burst
        pktsInBurst = pktsInBurst + 1
        burstSize = burstSize + pktLen
        ts_prev = ts
        len_prev = pktLen
        burstLastPacketId = packetId
        if key in flowID.keys():
            flowID[key][0] = flowID[key][0] + 1
            flowID[key][1] = flowID[key][1] + pktLen
        else:
            flowID[key] = [1]
            flowID[key].append(pktLen)
    else:
        #find look into the burst and find out the flow with the max number of bytes
        k = flowID.items()[0][0]
        mx_bytes = flowID[k][1]
        mx_k = k
        for k in flowID.keys():
            if(flowID[k][1] > mx_bytes):
                mx_bytes = flowID[k][1]
                mx_k = k
        
        maxBytesPkt = flowID[mx_k][0]        
        #print burst details
        op = str(burstLastPacketId) +  ',' + str(burstId) + ","+ str(burstSize) + "," + str(pktsInBurst) + "," +\
        str(maxBytesPkt) + "," + str(mx_bytes) + "," + str(mx_bytes/burstSize)
	f.write(op+"\n")
        #print("\n")
        #Now we should start a new burst
        burstLastPacketId = packetId
        burstId = burstId + 1
        pktsInBurst = 1
        burstSize = pktLen
        burstBeginTime = ts_now
        ts_prev = ts_now
        flowID = {}
        flowID[key] = [1]
        flowID[key].append(pktLen)
f.close()
