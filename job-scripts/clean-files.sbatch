#!/bin/bash

#SBATCH -J clean_input_data  # A single job name for the array
#SBATCH -n 1
#SBATCH -t 00:10:00
#SBATCH -p serial
#SBATCH --mem 3000

cat $1 | sed 's/\->//g' | awk 'BEGIN {FS = " "} ; { print $1 "," $2 "," $3 "," $4 "," $5 "," $6 "," $7 "," $8}' > $2

