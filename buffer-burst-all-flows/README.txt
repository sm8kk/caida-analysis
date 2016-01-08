Process for generating the results from the input data:
Generate the ASCII file or tshark output from the pcap file using:

1) tshark -o column.format:'"No.", "%m", "Time", "%t", "Source", "%s", "Destination", "%d", "srcport", "%uS", "dstport", "%uD", "len", "%L", "Protocol", "%p"' -r file.pcap > tshark-out.txt
As an example usecase only considering the first 10000 packets of the output
2) head -10000 tshark-out.txt > tshark-10k.txt

Clean the tshark data using:
1) cat tshark-10k.txt | sed 's/\->//g' | awk 'BEGIN {FS = " "} ; { print $1 "," $2 "," $3 "," $4 "," $5 "," $6 "," $7 "," $8}' > packets-10k.txt
2) some rows have packet data fields missing (which we cannot use), take these out using: cat packets-10k.txt | grep -v ,, > packets-10k-cleaned.txt

Go into the software directory and:
3) Run the code by: python find-max-packets-flow-in-burst.py ../data/packets-10k-cleaned.txt > ../results/burst-10kpkts.txt
