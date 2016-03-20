# -*- coding: utf-8 -*-
"""
@author: souravmaji
"""
import sys

# Open the file
f = open(str(sys.argv[1]), 'r')

# Read ALL the lines (you can also iterate if you like)
# Each line is stored as an element of the "list" lines
lines = f.readlines()

# Close the file
f.close()

# Parse the lines and creates a dictionary where the key is given by the hash
# of the first 5 fields and the value a list of all the fields. Also create a
# set of the hashes. This method relies on a 1-to-1 correspondence between the
# hash and the data in the first 5 fields which might not be assured. You might
# what to check other hashing options (hashlib).
data1 = {}
data_set1 = set()
for l in lines:  # For every line in the file
    values = l.split()  # Create a tuple (immutable list) from the fields
    h = values[0]+values[1]+values[2]+values[3]+values[4]
#    h = hash(values[:5])  # Evaluate the hash (unique in this direction) from the first 5 fields
    data_set1.add(h)  # Add the hash to the set
    data1[h] = values  # Add the data to the dictionary using the hash as index

#print('\n--- Data1 ---')
#print(data1)

f = open(str(sys.argv[2]), 'r')
lines = f.readlines()
f.close()

data2 = {}
data_set2 = set()
for l in lines:
    values = l.split()  # Create a tuple (immutable list) from the fields
    h = values[0]+values[1]+values[2]+values[3]+values[4]
    data_set2.add(h)
    data2[h] = values

#print('\n--- Data2 ---')
#print(data2)

data3 = {}

# file1 is the first 'n' packets
# file2 is the next 'm' packets
# data3 is the combined flow record
# for simplicity we do not check a time bound for a flow

# fill flow data from previous packets
j = 0
file1_diff_file2 = data_set1 - data_set2
for i in file1_diff_file2:
    data3[j] = data1[i]
    j = j + 1
    
k = j
print('\n -- Data1 part of data3 :')
print(j)    
#print('\n--- Common data ---')

# flows from the previous minute that match the flowID's in the current minute.
# For the common_set the following cases has to be checked:
# (i) Since it is common data, it means that the flow begining has already been found
# so, we update the byteCount, pktCount, endTm and maybe the FIN flag.
# (ii) While updating if a FIN is observed, the flow should be ended. Print out
# FIN terminated end flows.
# (iii) A timeout of a flow can be seen after it is inactive for sometime (~60 seconds)
# timeout-terminated-flows.
# Anomalous cases:
# (i) In the i th minute, if no FIN is seen, but in the (i+1) th minute a SYN or SYN/ACK is seen.
# How do we handle such flows?
# (ii) In the i th minute, if no FIN is seen, but in the (i+1) th minute a RST is seen.

# TODO: Incorporate all these conditions in this check
common_set = data_set1 & data_set2  # Evaluate the intersection of the hash sets
for i in common_set:  # For each element in the intersection, print the data form the two sets
    data3[j] = data1[i]
    data3[j][5] = str(long(data1[i][5]) + long(data2[i][5]))
    data3[j][6] = str(long(data1[i][6]) + long(data2[i][6]))
    data3[j][8] = data2[i][8] # update the last timestamp
    data3[j][9] =str(max((long(data1[i][9])), (long(data2[i][9]))))
    data3[j][10] =str(min((long(data1[i][10])), (long(data2[i][10]))))
    data3[j][11] = str(long(data1[i][11]) + long(data2[i][11]))
    data3[j][12] = str(long(data1[i][12]) + long(data2[i][12]))
    data3[j][13] = str(long(data1[i][13]) + long(data2[i][13]))
    data3[j][14] = str(long(data1[i][14]) + long(data2[i][14]))
    data3[j][15] = str(long(data1[i][15]) + long(data2[i][15]))
    data3[j][16] = str(long(data1[i][16]) + long(data2[i][16]))
    data3[j][17] = str(long(data1[i][17]) + long(data2[i][17]))
    data3[j][18] = str(long(data1[i][18]) + long(data2[i][18]))
    data3[j][19] = str(long(data1[i][19]) + long(data2[i][19]))
    data3[j][20] = str(long(data1[i][20]) + long(data2[i][20]))
    data3[j][21] = str(long(data1[i][21]) + long(data2[i][21]))
    data3[j][22] = str(long(data1[i][22]) + long(data2[i][22]))
    data3[j][23] = str(long(data1[i][23]) + long(data2[i][23]))
    data3[j][24] = str(long(data1[i][24]) + long(data2[i][24]))
    data3[j][25] = str(long(data1[i][25]) + long(data2[i][25]))
    data3[j][26] = str(long(data1[i][26]) + long(data2[i][26]))
    
    j = j + 1
    #print(data2[i])
    #print('---')

l = j
print('\n -- common part of data3 :')
print(j - k)    

file2_diff_file1 = data_set2 - data_set1
for i in file2_diff_file1:
    data3[j] = data2[i]
    j = j + 1


print('\n -- Data2 part of data3 :')
print(j - l)
    
#print('\n-- Data3 --')
#print(data3)

import csv

with open(sys.argv[3], 'wb') as f:  # Just use 'w' mode in 3.x
   w = csv.writer(f, delimiter=' ', quotechar=' ')
   w.writerows(data3.values())
