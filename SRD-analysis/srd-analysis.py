# -*- coding: utf-8 -*-
from __future__ import division
import sys



'''
This program is for looking into the size, rate and duration
of the packets in the first minuts

The input file has the following format
flowID,byteCount,pkts,beginTm,endTm,SYN,SYNACK,FIN,RTT
88.118.250.239-178.106.209.97-49165-80,46980,256,1403182864446073,1403182936377687,1,0,0,98533

'''


'''
Author: Austin
Created on: March 8th
'''


with open(sys.argv[1], 'r') as fileone:
	lines = fileone.readlines()



fileTwo = open(sys.argv[2],'w') #writes SRD info of all flows
fileTwo.write("FlowID,bytes,pkts,beginTime,endTime,SYN,SYNACK,FIN,dur,rate,RTT\n") 


fileThree = open(sys.argv[3],'w') #writes SRD info of flows for, which we can measure a RTT
fileThree.write("FlowID,bytes,pkts,beginTime,endTime,SYN,SYNACK,FIN,dur,rate,RTT\n") 

fileFour = open(sys.argv[4],'w') #writes SRD info of flows for, which we can measure a RTT (but within a range of 0 to 1.5secs)
fileFour.write("FlowID,bytes,pkts,beginTime,endTime,SYN,SYNACK,FIN,dur,rate,RTT\n") 
skipFirst=1
#count=0

for l in lines:
    #count = count + 1
    if skipFirst==1:
        skipFirst=0
        continue;

    val = l.split(",")
    if len(val) != 9:
        continue;
    #print count
    size = int(val[1])
    dur = float(val[4]) - float(val[3])
    
    if (dur <= 0):
        continue;

    rate = float(size*8*1000000/dur)
    fin = int(val[7])
    rtt = float(val[8])
    RTT = (rtt/1000) #RTT is in milliseconds
    op = val[0] + "," + val[1]+ "," + val[2] + "," + val[3] + "," +\
         val[4]+ "," + val[5] + "," + val[6] + "," + str(fin) + "," +\
         str(float(dur/1000000)) + "," + str(rate) + "," + str(RTT) + "\n"
    
    fileTwo.write(op)
    if(RTT > 0):
        fileThree.write(op)

    if(RTT > 0 and RTT < 1500):
	fileFour.write(op) 

fileTwo.close()
fileThree.close()
fileFour.close()

