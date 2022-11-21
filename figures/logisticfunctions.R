logistic <- function(x) exp(x)/(1 + exp(x))
x <- rnorm(1000,5,1)
x_std <- x - mean(x)

plot(x_std,logistic(x_std))
plot(x_std,logistic(x_std - 1))

plot(x_std,logistic(-x_std))
plot(x_std,logistic(-x_std - 1))

plot(x_std,logistic(abs(x_std)))
plot(x_std,logistic(abs(x_std) - 0.75))
plot(x_std,logistic(abs(x_std) - 0.75 - 1))

plot(x_std,logistic(-abs(x_std)))
plot(x_std,logistic(-abs(x_std) + 0.75))
plot(x_std,logistic(-abs(x_std) + 0.75 - 1))

sum(logistic(x_std))
sum(logistic(-abs(x_std) + 0.75))     
