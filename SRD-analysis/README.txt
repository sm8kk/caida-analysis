Usage:

python srd-analysis.py <path to completed 61min flows>  <op file for SRD measure of all the flows>
Flows with duration as 0 are ignored. 

Modified version:
time python srd-analysis.py ../../caida-analysis-results/completedFlow/completed-flows61min.txt ../../caida-analysis-results/completedFlow/srdAllFlows.txt ../../caida-analysis-results/completedFlow/srdRttFlows.txt

or

time python srd-analysis.py ../../caida-analysis-results/completedFlow/completed-flows61min.txt ../../caida-analysis-results/completedFlow/srdAllFlows.txt ../../caida-analysis-results/completedFlow/srdRttFlows.txt ../../caida-analysis-results/completedFlow/srdRttBoundedFlows.txt

or 
python srd-analysis.py sample-analysis.txt srd.txt srdRtt.txt
