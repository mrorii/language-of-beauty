library(ggplot2)
options(scipen=999)

args <- commandArgs(trailingOnly=TRUE)
inputFile <- args[1]
outputFile <- args[2]

prices <- read.csv(inputFile, header=TRUE, encoding="utf-8")

# Only look at "< 20" and "40's"
prices <- prices[prices$facet == "< 20" | prices$facet == "40's",]

# Reorder
prices$facet <- factor(prices$facet, as.character(
  c("< 20", "40's")
))

ggplot(prices, aes(price, color=facet)) +
  geom_line(stat="density") +
  labs(x="Price", y="Density") +
  scale_x_continuous(breaks=seq(0,15000,by=1000), limits=c(0, 15500)) +
  theme(axis.text.x=element_text(angle=90, vjust=0.5)) +
  ggtitle("Price Distribution") +
  scale_color_discrete(name="Age Group")

ggsave(outputFile, scale=0.8)
