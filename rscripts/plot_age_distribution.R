library(ggplot2)

args <- commandArgs(trailingOnly=TRUE)
inputFile <- args[1]
outputFile <- args[2]

age <- read.csv(inputFile, header=TRUE)

# Re-order the age groups
age$age_group <- factor(age$age_group, as.character(
  c("< 20", "Early 20's", "Late 20's", "Early 30's", "Late 30's",
    "40's", ">= 50's")
))

ggplot(age, aes(x=age_group, y=count)) +
  geom_bar(stat="identity", show.legend=FALSE, color="#E08A99", fill="#F2C7CE") +
  labs(x="Age Group", y="Number of Users") +
  ggtitle("User Age Distribution")

ggsave(outputFile, scale=0.8)
