args<-commandArgs()
filename=args[6]
opfile1=args[7]
opfile2=args[8]
print(filename)
print(opfile1)
print(opfile2)

setwd("/if13/sm8kk/caida-analysis-results/delta10ns")
library(ggplot2)
bursts=read.csv(filename, header=T)
#bursts=read.csv("burst-cdf-data.csv", header=T)

# Burst size CDF

plot1<-ggplot(bursts, aes(burstSize)) + stat_ecdf() + theme_bw() +
  xlab("Burst Size") + ylab("CDF") +
theme(axis.title = element_text(size=15, face="bold"), axis.text=element_text(size=20, face="bold"))

ggsave(plot1, file=opfile1, width=10, height=10)
# Packets in a burst CDF

plot2<-ggplot(bursts, aes(pktsInBurst)) + stat_ecdf() + theme_bw() +
  xlab("Packets in Burst") + ylab("CDF") +
  theme(axis.title = element_text(size=15, face="bold"), axis.text=element_text(size=20, face="bold"))

ggsave(plot2, file=opfile2, width=10, height=10)

