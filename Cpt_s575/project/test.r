library(dplyr)
library(tidyr)

## data <- read.csv('https://scads.eecs.wsu.edu/wp-content/uploads/2017/10/AM_strains_clean.csv', na.string = '?')
data <- read.csv('~/Documents/wsu/Cpt_s575/project/data/AM_strains_clean.csv', na.string='?', fileEncoding='utf-16', sep='\t')

head(data)