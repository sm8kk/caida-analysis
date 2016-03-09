# -*- coding: utf-8 -*-
from __future__ import division
import sys



'''
This program is for looking into the size, rate and duration
of the packets in the first minuts

The input file has the following format
1,0.000000000,39.196.79.86,201.65.11.34,80,49459,1404,1403182800.000001000,0x0010

'''


'''
Author: Austin
Created on: March 8th
'''

with open(sys.argv[1], 'r') as fileone:
	lines = fileone.readlines()


print "fileone is readed"

fileTwo = open(sys.argv[2],'w')
fileTwo.write("flowId, firstTime, lastTime, numPkts, numBytes, SYN, FIN\n") 


print "filetwo is opened"

flowDict={}
# The key in the dictionary will be the flowIp and the value of the key will be a list of strings
# which contains flowBeginTime, flowEndTime, numberofPackets, flowSize

flowNumber = 1
# for a SYN segment flags=2
SYN=2 # the flags value has to be 0x0002
FIN=1 # here only the last bit is 1

# This represents the Id of the flow


for l in lines:
	val = l.split(",")
	pktTm = val[1]
	flowID = val[2] + "-" + val[3] + "-" + val[4] + "-" + val[5]
	pktLen = int(val[6])
	pktFlgStr = val[8][:-1]
        pktFlg = int(pktFlgStr, 16) #converting the flag from string to integer; string is in hex so 16 is used.

	if (pktFlg == SYN):
		# We should initialize this flowIp in the dictionary
		flowDict[flowID] = [pktTm, pktTm, 1, pktLen, 1, 0]
		continue

	if (flowID in flowDict.keys()):
		# This flow is not ended and we should update it
		flowDict[flowID][1] = pktTm # [1] is the endtime
		flowDict[flowID][2] = flowDict[flowID][2] + 1 #updating the number of packets, which is [2]
		flowDict[flowID][3] = flowDict[flowID][3] + pktLen #updating the number of bytes trnsferred by the flow [3]
		flowDict[flowID][5] = pktFlg & FIN #Update the fin flag if there is one

print "The number of flows is :" + str(len(flowDict))
		

# Now we have already gone through the file. The flowDict contains the flows which has not ended in this minute
# We should print it out now
for flowID in flowDict.keys():
	outputString = flowID + "," + flowDict[flowID][0] + "," + flowDict[flowID][1] + "," + \
        str(flowDict[flowID][2]) + "," + str(flowDict[flowID][3]) + "," + str(flowDict[flowID][4]) + "," + str(flowDict[flowID][5]) + "\n"
        fileTwo.write(outputString)
fileTwo.close()


