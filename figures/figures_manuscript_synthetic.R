library(ggplot2)
library(tidyverse)

setwd("C:/Users/20200059/Documents/Github/missingness-effect-complete-dataset/figures/")

result <- read_csv("../csvs/final/synthetic.csv")
head(result)

result <- result %>%
  mutate(type = ordered(factor(type), 
                        levels = c('MCAR','LEFT','MID','TAIL','RIGHT')))

skews <- result %>%
  group_by(mech, type, skew) %>%
  summarize(am = mean(amount)) %>%
  filter(skew == 'yes')
skews

# bias mean
plot <- result %>%
  filter(skew != 'diff') %>%
    ggplot(aes(y=mean, x=mech, fill=skew)) +
      geom_boxplot(outlier.shape=NA)+
      geom_boxplot(aes(color=skew),outlier.shape = NA) + 
      facet_grid(. ~ type, labeller = label_both, scales = "free") +
      labs(title = 'Mean shift',
           fill = 'skew') + 
      xlab('mechanism') + 
      ylab('') + 
  guides(fill = guide_legend(direction = "horizontal")) +
  theme(legend.position="top",
        legend.justification="right",
        plot.title = element_text(vjust=-10)) + 
  scale_fill_manual(values=c("#e34a33", "#1a9641")) + 
  scale_color_manual(values=c("#e34a33", "#1a9641"))

plot
name <- paste('synthetic-bias.pdf', sep = "", collapse = NULL)
ggsave(name, width = 20, height = 12, units = "cm")

result %>%
  filter(skew == 'diff') %>%
    ggplot(aes(y=mean, x=type, colour=mech)) + 
      geom_boxplot(outlier.shape = NA) 
        #+ scale_y_continuous(limits = quantile(result$mean, c(0.1,0.9)))

# bias sd
plot <- result %>%
  filter(skew != 'diff') %>%
  ggplot(aes(y=sd, x=mech, fill=skew)) +
  geom_boxplot(outlier.shape=NA)+
  geom_boxplot(aes(color=skew),outlier.shape = NA) + 
  facet_grid(. ~ type, labeller = label_both, scales = "free") +
  labs(title = 'Standard deviation shift',
       fill = 'skew') + 
  xlab('mechanism') + 
  ylab('') + 
  guides(fill = guide_legend(direction = "horizontal")) +
  theme(legend.position="top",
        legend.justification="right",
        plot.title = element_text(vjust=-10)) + 
  scale_fill_manual(values=c("#e34a33", "#1a9641")) + 
  scale_color_manual(values=c("#e34a33", "#1a9641"))

plot
name <- paste('synthetic-std.pdf', sep = "", collapse = NULL)
ggsave(name, width = 20, height = 12, units = "cm")

result %>%
  filter(skew == 'diff') %>%
  ggplot(aes(y=sd, x=type, colour=mech)) + 
  geom_boxplot(outlier.shape = NA) 
    + scale_y_continuous(limits = quantile(result$sd, c(0.1,0.9)))

# bias median
result %>%
  filter(skew != 'diff') %>%
  ggplot(aes(y=median, x=mech, colour=skew)) + 
  geom_boxplot(outlier.shape = NA) + 
  facet_grid(. ~ type, labeller = label_both) 
    + scale_y_continuous(limits = quantile(result$median, c(0.1,0.9)))

result %>%
  filter(skew == 'diff') %>%
  ggplot(aes(y=median, x=type, colour=mech)) + 
  geom_boxplot(outlier.shape = NA) 
    + scale_y_continuous(limits = quantile(result$median, c(0.1,0.9)))

# iqr
result %>%
  filter(skew != 'diff') %>%
  ggplot(aes(y=iqr, x=mech, colour=skew)) + 
  geom_boxplot(outlier.shape = NA) + 
  facet_grid(. ~ type, labeller = label_both) 
    + scale_y_continuous(limits = quantile(result$iqr, c(0.1,0.9)))

result %>%
  filter(skew == 'diff') %>%
  ggplot(aes(y=iqr, x=type, colour=mech)) + 
  geom_boxplot(outlier.shape = NA) 
    + scale_y_continuous(limits = quantile(result$iqr, c(0.1,0.9)))

# skew
result %>%
  filter(skew != 'diff') %>%
    ggplot(aes(y=amount, x=mech, colour=skew)) + 
      geom_boxplot(outlier.shape = NA) + 
      facet_grid(. ~ type, labeller = label_both) + 
      scale_y_continuous(limits = quantile(result$amount, c(0.1,0.9)))
