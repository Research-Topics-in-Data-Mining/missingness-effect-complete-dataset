library(MASS)
library(mice)
library(tidyverse)

setwd("C:/Users/20200059/Documents/Github/missingness-effect-complete-dataset/")

# set up simulation

T = 1000
N = 10000
mechs = c("MCAR", "MAR", "MNAR")
types = c("RIGHT", "LEFT", "MID", "TAIL")
result = as.data.frame(matrix(NA, nrow=T*3*4*3, ncol=8))
colnames(result) = c('mech', 'type', 'skew', 'amount', 'mean', 'sd', 'median', 'iqr')

logistic <- function(x) exp(x)/(1 + exp(x))

# create data

i <- 1
for(t in 1:T){
  for(j in 1:3){
    for(k in 1:4){
    
      print(i)
      mech <- mechs[j]
      type <- types[k]
      
      if(mech == "MCAR"){
        type <- NULL
        wtype <- mech
      } else {
        wtype <- type
      }
      
      # create data
      data <- as.data.frame(mvrnorm(mu = c(10,10), 
                                    Sigma=matrix(data = c(1,0.5,0.5,1), byrow=TRUE, nrow=2),
                                    n = N))
      colnames(data) <- c('A','B')
      
      # create skewed data
      data_skew <- data
      idx <- which(data_skew$A > (mean(data_skew$A) + 3*sd(data_skew$A)))
      data_skew[idx, 'A'] <- data_skew[idx, 'A']^2
      
      # standardize both datasets to make sure they have the same mean and std
      data$A <- (data$A - mean(data$A))/sd(data$A)
      data_skew$A <- (data_skew$A - mean(data_skew$A))/sd(data_skew$A)
      
      # calculate skew
      skew_data <- (3*(mean(data$A) - median(data$A))) / sd(data$A)
      skew_data_skew <- (3*(mean(data_skew$A) - median(data_skew$A))) / sd(data_skew$A)
      
      # start with non-skewed data
      mean_true <- mean(data$A)
      sd_true <- sd(data$A)
      median_true <- median(data$A)
      iqr_true <- IQR(data$A)
  
      data_amp <- ampute(data, prop = 0.5,
                         patterns = matrix(c(0, 1), byrow=TRUE, nrow=1), 
                         mech = mech, type = type)$amp
      
      data_mean <- mean(data_amp$A, na.rm = TRUE)
      data_sd <- sd(data_amp$A, na.rm = TRUE)
      data_median <- median(data_amp$A, na.rm=TRUE)
      data_iqr <- IQR(data_amp$A, na.rm=TRUE)
      
      #bias_mean <- (data_mean - mean_true)/mean_true
      #bias_sd <- (data_sd - sd_true)/sd_true
      #bias_median <- (data_median - median_true)/median_true
      #bias_iqr <- (data_iqr - iqr_true)/iqr_true
      
      bias_mean <- (data_mean - mean_true)
      bias_sd <- (data_sd - sd_true)
      bias_median <- (data_median - median_true)
      bias_iqr <- (data_iqr - iqr_true)
    
      result[i,] <- c(mech, wtype, 'no', round(skew_data,4), 
                      round(bias_mean,4), round(bias_sd,4),
                      round(bias_median,4), round(bias_iqr,4))
      i = i + 1

      # follow with skewed data
  
      mean_skew_true <- mean(data_skew$A)
      sd_skew_true <- sd(data_skew$A)
      median_skew_true <- median(data_skew$A)
      iqr_skew_true <- IQR(data_skew$A)
    
      data_amp_skew <- ampute(data_skew, prop = 0.5,
                              patterns = matrix(c(0, 1), byrow=TRUE, nrow=1), 
                              mech = mech, type=type)$amp
    
      data_mean_skew <- mean(data_amp_skew$A, na.rm = TRUE)
      data_sd_skew <- sd(data_amp_skew$A, na.rm = TRUE)
      data_median_skew <- median(data_amp_skew$A, na.rm = TRUE)
      data_iqr_skew <- IQR(data_amp_skew$A, na.rm = TRUE)
      
      #bias_mean_skew <- (data_mean_skew - mean_skew_true)/mean_skew_true
      #bias_sd_skew <- (data_sd_skew - sd_skew_true)/sd_skew_true
      #bias_median_skew <- (data_median_skew - median_skew_true)/median_skew_true
      #bias_iqr_skew <- (data_iqr_skew - iqr_skew_true)/iqr_skew_true
      
      bias_mean_skew <- (data_mean_skew - mean_skew_true)
      bias_sd_skew <- (data_sd_skew - sd_skew_true)
      bias_median_skew <- (data_median_skew - median_skew_true)
      bias_iqr_skew <- (data_iqr_skew - iqr_skew_true)

      result[i,] <- c(mech, wtype, 'yes', round(skew_data_skew,4), 
                      round(bias_mean_skew,4), round(bias_sd_skew,4),
                      round(bias_median_skew,4), round(bias_iqr_skew,4))
      i = i + 1
      
      result[i,] <- c(mech, wtype, 'diff', round(skew_data - skew_data_skew,4), 
                      round(bias_mean_skew - bias_mean,4), 
                      round(bias_sd_skew - bias_sd,4),
                      round(bias_median_skew - bias_median,4), 
                      round(bias_iqr_skew - bias_iqr,4))
      
      i = i + 1
    }
  }
}

result <- result %>% mutate(mean = as.numeric(mean), sd = as.numeric(sd), 
                            amount = as.numeric(amount),
                            median = as.numeric(median),
                            iqr = as.numeric(iqr))
write.csv(result,"./csvs/final/synthetic.csv", row.names = FALSE)


