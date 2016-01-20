#!/bin/bash
# usage ./tshark-screen.sh file.txt <-- file.txt contains the names of pcap files and it is preferred that it contain only 4 filenames

file=$1
INDIR="~/data/CAIDA_traces/2014-traces/raw_files"
OPDIR="~/tshark-60min-caida-all-pkts"

while read filename
do
    echo Working on file $INDIR/$filename ..
    f2=`echo $filename | rev | cut -c 15- | rev`
    f3=".txt"
    f4=${f2}${f3}
    #tshark -o column.format:'"No.", "%m", "Time", "%t", "Source", "%s", "Destination", "%d", "srcport", "%uS", "dstport", "%uD", "len", "%L", "Protocol", "%p"' -r file.pcap > tshark-out.txt
    echo Executing : screen -mdS $f2 zsh -c "time ./tshark -r $INDIR/$filename -o column.format:'"No.", "%m", "Time", "%t", "Source", "%s", "Destination", "%d", "srcport", "%uS", "dstport", "%uD", "len", "%L", "Protocol", "%p"'> $OPDIR/$f4"
    screen -mdS $f2 zsh -c "time ./tshark -r $INDIR/$filename -o column.format:'"No.", "%m", "Time", "%t", "Source", "%s", "Destination", "%d", "srcport", "%uS", "dstport", "%uD", "len", "%L", "Protocol", "%p"'> $OPDIR/$f4"
done < $file
