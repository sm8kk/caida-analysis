#!/bin/bash
#usage file should be from next minute to the last minute.
#Usage: ./concatenate.sh <filenames-of-ncfiles-1st-to-60thmin> <0th-min-ncflows-filename>

file=$1 #this is the names of files

NCDIR="/if13/sm8kk/caida-analysis-results/ncompletedFlow"
CDIR="/if13/sm8kk/caida-analysis-results/completedFlow"
#TNCDIR="/if13/sm8kk/caida-analysis-results/ncompletedFlowTill"
#TCDIR="/if13/sm8kk/caida-analysis-results/completedFlowTill"
PROG="../concatenate/concatenate.py"

fth=$2 #this is the starting file, should not be included in file.

while read filename #filename should have all files from 1stmin to 60th min
do
        echo Working on file $INDIR/$filename
	f=`echo $filename | cut -c 1-6`
	fcom=${f}_tillCom.txt
	fnc=${f}_tillNc.txt
	echo Executing : time python $PROG $NCDIR/$fth $NCDIR/$filename $CDIR/$fcom $NCDIR/$fnc 120
	time python $PROG $NCDIR/$fth $NCDIR/$filename $CDIR/$fcom $NCDIR/$fnc 120
	fth=$fnc
	sleep 1s
done < $file


