# Python script which calculates the time interval of flows.
from __future__ import division
import sys

with open(sys.argv[1], 'r') as fileone:
        lines = fileone.readlines()


fileTwo = open(sys.argv[2],'w')
fileTwo.write("pktTmOff\n")

tm =[]
skipFirstLine = 0
for l in lines:
    val = l.split(",")
    if skipFirstLine == 0:
        skipFirstLine = 1
	continue;

    pktTm = float(val[1])
    tm.append(pktTm);

for i in xrange(len(tm)-1):
    offset = tm[i+1] - tm[i]
    fileTwo.write(str(offset)+"\n")

fileTwo.close()
