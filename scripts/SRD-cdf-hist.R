args<-commandArgs()
filename=args[6]
print(filename)
setwd("/if13/sm8kk/caida-analysis/scripts")
library(ggplot2)
#flows=read.csv("../anl/allflows-data-http-scp-oth/79.217.69.9-68.14.83.150-683-3152-scp.csv", header=T)
flows=read.csv(filename, header=T)
mnRate=mean(flows$rate)
sdRate=sd(flows$rate)
#rangeRt=max(flows$rate)-min(flows$rate)


plot1<-ggplot(data=flows, aes(rate)) + 
  geom_histogram(aes(fill = ..count..)) + scale_x_log10() + theme_bw() + xlab("Rate in bps") + ylab("Frequency") +
theme(axis.title = element_text(size=15, face="bold"), axis.text=element_text(size=20, face="bold"))

ggsave(plot1, file="histRate.png", width=10, height=10)

#plot2<-ggplot(flows, aes(rate)) + stat_ecdf() + scale_x_log10() + theme_bw() +
#  xlab("Rate (bps)") + ylab("CDF") +
#theme(axis.title = element_text(size=15, face="bold"), axis.text=element_text(size=20, face="bold"))

#ggsave(plot2, file="cdfRate.png", width=10, height=10)

mnDur=mean(flows$dur)
sdDur=sd(flows$dur)
#rangeDur=max(flows$dur)-min(flows$dur)

plot3<-ggplot(data=flows, aes(dur)) + 
  geom_histogram(aes(fill = ..count..)) + scale_x_log10() + theme_bw() + xlab("Duration in secs") + ylab("Frequency") +
theme(axis.title = element_text(size=15, face="bold"), axis.text=element_text(size=20, face="bold"))

ggsave(plot3, file="histDur.png", width=10, height=10)

#plot4<-ggplot(flows, aes(dur)) + stat_ecdf() + scale_x_log10() + theme_bw() +
#  xlab("Duration (s)") + ylab("CDF") +
#theme(axis.title = element_text(size=15, face="bold"), axis.text=element_text(size=20, face="bold"))

#ggsave(plot4, file="cdfDur.png", width=10, height=10)


mnSz=mean(flows$bytes)
sdSz=sd(flows$bytes)

plot5<-ggplot(data=flows, aes(bytes)) + 
  geom_histogram(aes(fill = ..count..)) + scale_x_log10() + theme_bw() + xlab("Size in bytes") + ylab("Frequency") +
theme(axis.title = element_text(size=15, face="bold"), axis.text=element_text(size=20, face="bold"))

ggsave(plot5, file="histSize.png", width=10, height=10)

#plot6<-ggplot(flows, aes(bytes)) + stat_ecdf() + scale_x_log10() + theme_bw() +
#  xlab("Size (bytes)") + ylab("CDF") +
#theme(axis.title = element_text(size=15, face="bold"), axis.text=element_text(size=20, face="bold"))

#ggsave(plot6, file="cdfSize.png", width=10, height=10)

mnSz
sdSz
mnDur
sdDur
mnRate
sdRate

print("Size statistics:")
quantile(flows$bytes, c(0, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99, 1))

print("Rate statistics:")
quantile(flows$rate, c(0, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99, 1))

print("Duration statistics:")
quantile(flows$dur, c(0, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99, 1))

