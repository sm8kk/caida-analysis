#!/bin/bash
#usage: this is the starting minute file

file=$1

INDIR="/if13/sm8kk/flowFiles"
ABDIR="/if13/sm8kk/caida-analysis-results/abnormalFlow"
NCDIR="/if13/sm8kk/caida-analysis-results/ncompletedFlow"
CDIR="/if13/sm8kk/caida-analysis-results/completedFlow"
PROG="../pre-concatenate/extract-flowIDs-start-min.py"

while read filename
do
        echo Working on file $INDIR/$filename
	f=`echo $filename | cut -c 31-36`
	fab=${f}_ab.txt
	fcom=${f}_com.txt
	fnc=${f}_nc.txt
	echo Executing : time python $PROG $INDIR/$filename $ABDIR/$fab $CDIR/$fcom $NCDIR/$fnc 5
        time python $PROG $INDIR/$filename $ABDIR/$fab $CDIR/$fcom $NCDIR/$fnc 5
	sleep 1s
done < $file


