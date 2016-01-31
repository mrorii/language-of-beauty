library(ggplot2)
options(scipen=999)

args <- commandArgs(trailingOnly=TRUE)
inputFile <- args[1]
outputFile <- args[2]

scores <- read.csv(inputFile, header=TRUE)

number_ticks <- function(n) {
  function(limits) pretty(limits, n)
}

ggplot(scores, aes(x=rating, y=count)) +
  geom_bar(stat="identity", show.legend=FALSE, color="#C3D8D9", fill="#53A592") +
  labs(x="Score", y="Number of Reviews") +
  ggtitle("Review Score Distribution") +
  scale_x_continuous(breaks=number_ticks(8))

ggsave(outputFile, scale=0.8)
