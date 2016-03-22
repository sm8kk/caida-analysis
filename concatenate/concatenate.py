# -*- coding: utf-8 -*-
from __future__ import division
import sys

'''
This program is used for concatenating the flow of the new minute to the result of minutes before
'''


'''
Author: Sourav, Austin
Created on: Marth 20th
'''



'''
We have two input files, which are the flows continuing from minutes before and the new minute
The are in the format of:
FlowID,bytes,pkts,beginTime,endTime,SYN,SYNACK,FIN
90.92.84.195-232.182.6.134-22-62818,158105812,105647,1403182843307062,1403182859997842,0,1,0
90.92.84.167-56.146.229.68-22-65166,155513356,108354,1403182840140298,1403182859996938,0,1,0
181.39.159.122-51.13.80.108-5647-54058,61203352,40700,1403182804810007,1403182859981830,0,1,0


We have two output files, one is the completed flow, the other is the not completed flow.
The input parameter is the timeGap we set.
'''


with open(sys.argv[1], 'r') as fileOne:
	linesOne = fileOne.readlines()

# Create the dictionary and set of the 0 minute:
data0 = {}
data_set0 = set()

for i in range(1,len(linesOne)):
	l = linesOne[i]
	val = l.split(",")
	flowID = val[0]
	data_set0.add(flowID)
	data0[flowID] = val



with open(sys.argv[2], 'r') as fileTwo:
	linesTwo = fileTwo.readlines()

# Create the dictionary and set of the 1 minute:
data1 = {}
data_set1 = set()

for i in range(1,len(linesTwo)):
	l = linesTwo[i]
	val = l.split(",")
	flowID = val[0]
	data_set1.add(flowID)
	data1[flowID] = val


tmMin = int(linesTwo[2].split(",")[4])
minNum = int((tmMin - 1403182800000000)/60000000)
lastTS = 1403182800000000 + (minNum + 1) * 60000000  

fileThree = open(sys.argv[3], 'w') 
fileThree.write("flowID,byteCount,pkts,beginTm,endTm,SYN,SYNACK,FIN\n")
# We will put flow finished to this fileThree



fileFour = open(sys.argv[4], 'w')
fileFour.write("flowID,byteCount,pkts,beginTm,endTm,SYN,SYNACK,FIN\n")
# We will put flow not finished to this fileFour


timeGap = int(sys.argv[5]) * 1000000
# This time gap is for further discussion of data_set0 - data_set1




# Now we look into three cases:
# Case1: The flow in both 0min and 1min

for commonID in data_set0 & data_set1:
	bytesCount = int(data0[commonID][1]) + int(data1[commonID][1])
	pkts = int(data0[commonID][2]) + int(data1[commonID][2]) 
	beginTm = data0[commonID][3]
	endTm = data1[commonID][4]
	SYN = data0[commonID][5]
	SYNACK = data0[commonID][6]
	FIN = data1[commonID][7]
	outputline = commonID + "," + str(bytesCount) + "," + str(pkts) + "," + beginTm + "," + endTm + "," + SYN + "," + SYNACK + "," + FIN
	if (FIN == "1\n"): # Then we know that this flow ends in the later minute
		fileThree.write(outputline)
	else:
		fileFour.write(outputline)

for laterID in data_set1 - data_set0:
	flowID = data1[laterID][0]
        byteCount = data1[laterID][1]
        pkts = data1[laterID][2]
        beginTm = data1[laterID][3]
        endTm = data1[laterID][4]
       	SYN = data1[laterID][5]
        SYNACK = data1[laterID][6]
        FIN = data1[laterID][7]
	if (SYN == "1" or SYNACK == "1"):
		outputline = flowID + "," + byteCount + "," + pkts + "," + beginTm + "," + endTm + "," + SYN + "," + SYNACK + "," + FIN
		fileFour.write(outputline)

for formerID in data_set0 - data_set1:
	flowID = data0[formerID][0]
        byteCount = data0[formerID][1]
        pkts = data0[formerID][2]
        beginTm = data0[formerID][3]
        endTm = data0[formerID][4]
        SYN = data0[formerID][5]
        SYNACK = data0[formerID][6]
        FIN = data0[formerID][7]
	outputline = flowID + "," + byteCount + "," + pkts + "," + beginTm + "," + endTm + "," + SYN + "," + SYNACK + "," + FIN
	if (int(endTm) + timeGap > lastTS):
                fileFour.write(outputline)
	else:
		fileThree.write(outputline)




fileThree.close()
fileFour.close()































