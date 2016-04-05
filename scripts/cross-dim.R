args<-commandArgs()
filename=args[6]
print(filename)
setwd("/if13/sm8kk/caida-analysis/scripts")
library(ggplot2)
#flows=read.csv("srdRtt.txt", header=T)
flows=read.csv(filename, header=T)

# Histogram of RTT
plot1<-ggplot(data=flows, aes(RTT)) + 
  geom_histogram(aes(fill = ..count..)) + theme_bw() + xlab("RTT in ms") + ylab("Frequency") +
theme(axis.title = element_text(size=15, face="bold"), axis.text=element_text(size=20, face="bold"))

ggsave(plot1, file="histRTT.png", width=10, height=10)

#Cross dimensional analysis of RTT and data transferred
plot2<-ggplot(NULL, aes(RTT, bytes)) + 
  geom_point(data=flows, aes(color=rate), size=2) +
  scale_y_log10() +theme_bw() + xlab("RTT") + ylab("Size in Bytes") +
  theme(axis.title = element_text(size=15, face="bold"), axis.text=element_text(size=20, face="bold"))

ggsave(plot2, file="RttBytes.png", width=10, height=10)


#Cross dimensional analysis of RTT and rate
plot3<-ggplot(NULL, aes(RTT, rate)) + 
  geom_point(data=flows, color='blue', size=2) +
  scale_y_log10() +theme_bw() + xlab("RTT") + ylab("Rate in bps") +
  theme(axis.title = element_text(size=15, face="bold"), axis.text=element_text(size=20, face="bold"))

ggsave(plot3, file="RttRate.png", width=10, height=10)

#Cross dimensional analysis of RTT and duration
plot4<-ggplot(NULL, aes(RTT, dur)) + 
  geom_point(data=flows, color='blue', size=2) + theme_bw() + xlab("RTT") + ylab("Duration in sec") +
  theme(axis.title = element_text(size=15, face="bold"), axis.text=element_text(size=20, face="bold"))

ggsave(plot4, file="RttDur.png", width=10, height=10)

print("RTT statistics:")
quantile(flows$RTT, c(0, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99, 1))
