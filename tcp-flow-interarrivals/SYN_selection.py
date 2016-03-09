# -*- coding: utf-8 -*-
from __future__ import division
import sys


'''
This program is for looking into the flowId and time of the SYN packet

The input file has the following format
1,0.000000000,39.196.79.86,201.65.11.34,80,49459,1404,1403182800.000001000,0x0010

'''

'''
Author: Austin
Created on: March 8th
'''

with open(sys.argv[1], 'r') as fileone:
        lines = fileone.readlines()


fileTwo = open(sys.argv[2],'w')
fileTwo.write("flowId,packetTime\n")

for l in lines:
	val = l.split(",")
	packetFlag = val[8]
	if (packetFlag == "0x0002\n"):
		flowId = line[2] + "-" + line[3] + "-" + line[4] + "-" + line[5]
		packetTime = line[1]
		fileTwo.write(flowId + "," + packetTime + "\n")
fileTwo.close()












