library(MASS)

logistic <- function(x) exp(x)/(1 + exp(x))

# data
N = 10000
data <- as.data.frame(mvrnorm(mu = c(10,10), 
                              Sigma=matrix(data = c(1,0.5,0.5,1), byrow=TRUE, nrow=2),
                              n = N))
colnames(data) <- c('A','B')
hist(data$A, breaks=100)

skew_data <- (3*(mean(data$A) - median(data$A))) / sd(data$A)

mean(data$A)
sd(data$A)

data_std <- data
data_std$A <- (data_std$A - mean(data_std$A))/sd(data_std$A)

mean(data_std$A)
sd(data_std$A)

skew_data_std <- (3*(mean(data_std$A) - median(data_std$A))) / sd(data_std$A)

# create skew

data_skew <- data
idx <- which(data_skew$A > (mean(data_skew$A) + 3*sd(data_skew$A)))
data_skew[idx, 'A'] <- data_skew[idx, 'A']^2

hist(data_skew$A, breaks=100)
skew_data_skew <- (3*(mean(data_skew$A) - median(data_skew$A))) / sd(data_skew$A)

mean(data_skew$A)
sd(data_skew$A)

data_skew_std <- data_skew
data_skew_std$A <- (data_skew_std$A - mean(data_skew_std$A))/sd(data_skew_std$A)

mean(data_skew_std$A)
sd(data_skew_std$A)

skew_data_skew_std <- (3*(mean(data_skew_std$A) - median(data_skew_std$A))) / sd(data_skew_std$A)

