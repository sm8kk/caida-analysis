# This script invokes *.sbatch file, which submits a job to a/many nodes in rivanna
# It will pass input file name and output filename to the sbatch file
# It will run a loop as many as the number of files to be cleaned
# usage ./clean-files.sh file.txt <-- file.txt contains the names of pcap files.

file=$1
INDIR="/scratch/sm8kk/tshark-60min-caida-all-pkts"
OPDIR="/scratch/sm8kk/cleaned-tshark-60min-caida-all-pkts"

while read filename
do

    echo Working on file $INDIR/$filename ..
    echo " "
    echo "Executing : sbatch clean-files.sbatch $INDIR/$filename $OPDIR/$filename"
    sbatch clean-files.sbatch $INDIR/$filename $OPDIR/$filename
done < $file
