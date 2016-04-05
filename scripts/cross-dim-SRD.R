args<-commandArgs()
filename=args[6]
print(filename)
setwd("/if13/sm8kk/caida-analysis/scripts")
library(ggplot2)
#flows=read.csv("srdRtt.txt", header=T)
flows=read.csv(filename, header=T)

#Cross dimensional analysis of size and rate
plot2<-ggplot(NULL, aes(bytes, rate)) + 
  geom_point(data=flows, aes(color=dur), size=2) +
  scale_y_log10() + scale_x_log10() + theme_bw() + xlab("Size in Bytes") + ylab("Rate in bps") +
  theme(axis.title = element_text(size=15, face="bold"), axis.text=element_text(size=20, face="bold"))

ggsave(plot2, file="bytesRate.png", width=10, height=10)


#Cross dimensional analysis of size and duration
plot3<-ggplot(NULL, aes(bytes, dur)) + 
  geom_point(data=flows, color='blue', size=2) +
  scale_x_log10() + theme_bw() + xlab("Size in Bytes") + ylab("Duration in sec") +
  theme(axis.title = element_text(size=15, face="bold"), axis.text=element_text(size=20, face="bold"))

ggsave(plot3, file="BytesDur.png", width=10, height=10)

#Cross dimensional analysis of duration and rate
plot4<-ggplot(NULL, aes(dur, rate)) + 
  geom_point(data=flows, color='blue', size=2) + scale_y_log10() + theme_bw() + xlab("Duration in sec") + ylab("Rate in bps") +
  theme(axis.title = element_text(size=15, face="bold"), axis.text=element_text(size=20, face="bold"))

ggsave(plot4, file="durRate.png", width=10, height=10)

