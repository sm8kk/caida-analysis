# Merge all the files listed as names in file.txt
# Usage: ./merge-files.sh filenames.txt

file=$1
DIR=$2
fileMerged="merge-61min.txt"
touch $DIR/$fileMerged

while read filename
do
    echo Merging file $DIR/$filename
    cat $DIR/$filename >> $DIR/$fileMerged
done < $file
