# Merge all the files listed as names in file.txt
# Usage: ./merge-files.sh filenames.txt

file=$1
DIR="/if13/sm8kk/caida-analysis-results/completedFlow"
fileMerged="completed-flows61min.txt"
#touch $DIR/$fileMerged
count=1

while read filename
do
    echo Merging file $DIR/$filename

    if [[ $count -eq 1 ]]; then
        cat $DIR/$filename >> $DIR/$fileMerged
	#echo Hello
	#echo ""
    else
	cat $DIR/$filename | grep -v "FIN" >> $DIR/$fileMerged
	#echo World
	#echo ""
    fi
    count=$((count+1))
    sleep 1s
done < $file
