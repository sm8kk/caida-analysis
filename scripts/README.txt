Process of merging files:

1) ./merge-files.sh filenames.txt /if13/sm8kk/syn-packets-caida-61mins

for pre-concatenating:
1) ./pre-concatenate-start-min.sh flowFiles0min.txt > log-0min.txt
2) ./pre-concatenate-other-min.sh flowFiles1to30mins.txt > log1to30min.txt
3) ./pre-concatenate-other-min.sh flowFiles31to60mins.txt > log31to60min.txt

for concatenating files:
1) 130000_nc.txt: is the first fth or the second argument
run as : ./concatenate.sh ncFiles1to60min.txt 130000_nc.txt

Cross dim analysis:

1) time Rscript cross-dim.R ../../caida-analysis-results/completedFlow/srdRttBoundedFlows.txt > cross-dim-RTT-stats.txt
1) time Rscript cross-dim-SRD.R ../../caida-analysis-results/completedFlow/srdAllFlows.txt > cross-dim-SRD-stats.txt

