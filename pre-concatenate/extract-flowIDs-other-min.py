# -*- coding: utf-8 -*-
from __future__ import division
import sys

'''
This program is used for re-organized the output of the C++ program
and select out those flows which are likely to be a SYN flood attack
'''


'''
Author: Sourav, Austin

Created on: March 10th
Last modified on: Match 11th
'''

'''
The input data is of the format:
srcIP,srcPort,dstIP,dstPort,protocol,byteCount,pktCount,SYN,lastSynTm,bytesLastSynTm,SYN-ACK,lastSynAckTm,bytesLastSynAckTm,RST,lastRstTm,bytesLastRstTm,FIN,lastFinTm,bytesLastFinTm,firstTime,lastTime,synAckTmInt
90.92.84.195,22,232.182.5.39,38724,6,362250948,253385,SYN:0,0,0,SYN-ACK:1,1403182806770317,64,RST:0,0,0,FIN:1,1403182840068993,362250948,1403182806770317,1403182840068993,0
90.92.84.188,22,232.182.5.39,65014,6,334688364,234214,SYN:0,0,0,SYN-ACK:1,1403182800208717,64,RST:0,0,0,FIN:1,1403182832036839,334688364,1403182800208717,1403182832036839,0
222.91.105.172,27522,51.26.93.152,443,6,262364789,174544,SYN:0,0,0,SYN-ACK:0,0,0,RST:0,0,0,FIN:0,0,0,1403182800002315,1403182827730753,0

output file is in the format:
FlowID,byteCount,pktCount,beginTm,endTm,SYN,FIN

Identifies all TCP flows, no matter it starts in this minute or not

Also find when a TCP flow ends, which is indicated by the FIN flag. Otherwise, its the
packet with last timestamp.

In the process we have also identified anomalous flows; i.e. flows with many SYN's and
some flows with SYN and SYN/ACK.

for flows with only SYN's, which could be a SYN attack, we keep these rows in a different
file.
'''


tcpProt=6

with open(sys.argv[1], "r") as fileOne: #input file
	lines = fileOne.readlines()

fileTwo = open(sys.argv[2], 'w') 
# This fileTwo will record all the SYN flood attack flowID

fileThree = open(sys.argv[3], 'w')
fileThree.write("FlowID,bytes,pkts,beginTime,endTime,SYN,SYNACK,FIN\n")
# This fileThree will record all the flow ending in this minute, i.e FIN = 1 

fileFour = open(sys.argv[4], 'w')
fileFour.write("FlowID,bytes,pkts,beginTime,endTime,SYN,SYNACK,FIN\n")
# This fileFour will record all the flow left for further concatenating, i.e FIN = 0

tmGap = int(sys.argv[5])

tmMin = int(lines[2].split(",")[19])
minNum = int((tmMin - 1403182800000000)/60000000)
synTmTh = 1403182800000000 + minNum * 60000000 + (60-tmGap) * 1000000


tcpNum = 0
otherNum = 0

for i in range(1, len(lines)):
    l = lines[i]
    val = l.split(",")
    srcIP = val[0]
    srcPort = val[1]
    dstIP = val[2]
    dstPort = val[3]
    protocol = val[4]
    endTm = val[20]
    if (int(protocol) == tcpProt):	# We check whether this flow is a TCP flow first
        tcpNum = tcpNum + 1
        # The we check whether it is a SYN flood attack flow
	pktCount = int(val[6])		
	synNum = int((val[7].split(":"))[1])
	finNum = int((val[16].split(":"))[1])
	synAckTmInt = val[21]
        byteCount = int(val[5])  
        lastSynTm = int(val[8])
        lastSynAckTm = int(val[11])
        
        beginTm = 0
	if (lastSynTm > lastSynAckTm and lastSynTm > 0): # Then the flow begin with the SYN packet
            byteCount = byteCount - int(val[9]) + 64
            beginTm = lastSynTm
            synFlag = "SYN"
        elif (lastSynAckTm > lastSynTm and lastSynAckTm > 0):
            byteCount = byteCount - int(val[12]) + 64
            beginTm = lastSynAckTm
            synFlag = "SYNACK"
        else:
            synFlag = "OLD"
		
        if (synAckTmInt == "0\n" and beginTm < synTmTh and synFlag == "SYN"):#REDO: check for negative case of synAck
	    # Then we speculate it to be a SYN attack
	    fileTwo.write(l)
        else:
	    # This may not be a SYN attack
	    # We consider all flows, no matter it starts in this minute or not.
	    if (beginTm > 0):
	        SYN = 1
	    else:
		SYN = 0
		beginTm = int(val[19]) # Because this flow has already started, we should assign it a beginTm from the C++ output
		
	    if (synFlag == "SYN"):
		SYN_SYNACK = "1,0"
	    elif (synFlag == "SYNACK"):
		SYN_SYNACK = "0,1"
	    else:
		SYN_SYNACK = "0,0"
	    
            if (finNum != 0):
		FIN = 1
	    else:
		FIN = 0

   	    flowID = srcIP + "-" + dstIP + "-" + srcPort + "-" + dstPort

	
            if (FIN == 1 and synFlag != "OLD"): # The flow ended in this minute, output it to 
		outputLine = flowID + "," + str(byteCount) + "," + str(pktCount) + "," + str(beginTm) + "," + endTm + "," + SYN_SYNACK + "," + str(FIN) + "\n"
	  	fileThree.write(outputLine)
	    else:
		outputLine = flowID + "," + str(byteCount) + "," + str(pktCount) + "," + str(beginTm) + "," + endTm + "," + SYN_SYNACK + "," + str(FIN) + "\n"
                fileFour.write(outputLine)
    else:
        otherNum = otherNum + 1

fileTwo.close()
fileThree.close()
fileFour.close()

print " The minuite is: " + str(minNum) + "\n"
print " The threshold is " + str(synTmTh) + "\n"
print " The number of TCP flow is: " + str(tcpNum) + "\n"
print " The number of other flow is: " + str(otherNum) + "\n" 
