library(ggplot2)
library(readxl)
library(tidyverse)
library(RColorBrewer)
library(mice)
library(xtable)

setwd("C:/Users/20200059/Documents/Github/missingness-effect-complete-dataset/figures/")

#### Simulation results and figures for finalized manuscript ####

datam <- read_csv("../csvs/final/averages.csv")
datas <- read_csv("../csvs/final/stds.csv")
dataa <- read_csv("../csvs/final/values_all.csv")

datam <- datam %>%
  mutate(MCAR = ordered(factor(MCAR), levels = c(0,10,20))) %>%
  mutate(MAR = ordered(factor(MAR), levels = c(0,10,20))) %>%
  mutate(MNAR = ordered(factor(MNAR), levels = c(0,10,20)))

datas <- datas %>%
  mutate(MCAR = ordered(factor(MCAR), levels = c(0,10,20))) %>%
  mutate(MAR = ordered(factor(MAR), levels = c(0,10,20))) %>%
  mutate(MNAR = ordered(factor(MNAR), levels = c(0,10,20)))

datam <- cbind(datam,datas)
colnames(datam) <- c(names(datam[1:18]), paste0('std_', names(datam[1:18]), sep = "", collapse = NULL))

# bias for types
types = c('sigmoid-right', 'sigmoid-left', 'sigmoid-tail', 'sigmoid-mid')
for(i in 1:length(types)){
  stype = types[i]

  plot_data <- datam %>%
    filter(type == stype) %>%
    filter(MCAR == '10')
  
  bias <- plot_data %>%
    ggplot(aes(x = MNAR, y = bias, fill = MAR)) + 
    geom_bar(stat = "identity", position = position_dodge()) + 
    labs(title = paste(stype, sep = " ", collapse = NULL),
         fill = 'MAR') + 
    xlab('MNAR') + 
    ylab('Mean shift') +
    guides(fill = guide_legend(direction = "horizontal")) +
    theme(legend.position="top",
          legend.justification="right",
          plot.title = element_text(vjust=-4), 
          legend.box.margin = margin(-1,0,0,0, "line"),
          #axis.title.y = element_text(),
          panel.grid.major.x = element_blank(),
          panel.grid.minor.x = element_blank(),
          panel.grid.major.y = element_blank(),
          panel.grid.minor.y = element_blank()) + 
    scale_fill_manual(values=c("#deebf7", "#9ecae1", "#3182bd"))
  
  name <- paste('bias-', stype, '.pdf', sep = "", collapse = NULL)
  #name <- paste('bias-', stype, '.eps', sep = "", collapse = NULL)
  ggsave(name, width = 20, height = 24, units = "cm")
}

# std for types
#types = c('sigmoid-right')
types = c('sigmoid-right', 'sigmoid-left', 'sigmoid-tail', 'sigmoid-mid')
for(i in 1:length(types)){
  stype = types[i]
  
  plot_data <- datam %>%
    filter(type == stype) %>%
    filter(MCAR == '10')
  
  std <- plot_data %>%
    ggplot(aes(x = MNAR, y = bias_std, fill = MAR)) + 
    geom_bar(stat = "identity", position = position_dodge()) + 
    labs(title = paste(stype, sep = " ", collapse = NULL),
         fill = 'MAR') + 
    xlab('MNAR') + 
    ylab('Standard deviation shift') +
    guides(fill = guide_legend(direction = "horizontal")) +
    theme(legend.position="top",
          legend.justification="right",
          plot.title = element_text(vjust=-4), 
          legend.box.margin = margin(-1,0,0,0, "line"),
          #axis.title.y = element_text(),
          panel.grid.major.x = element_blank(),
          panel.grid.minor.x = element_blank(),
          panel.grid.major.y = element_blank(),
          panel.grid.minor.y = element_blank()) + 
    scale_fill_manual(values=c("#deebf7", "#9ecae1", "#3182bd")) + 
    scale_y_continuous(limits = c(-0.015, 0.015))

  name <- paste('std-', stype, '.pdf', sep = "", collapse = NULL)
  #name <- paste('std-', stype, '.eps', sep = "", collapse = NULL)
  ggsave(name, width = 20, height = 24, units = "cm")
}

# combination bias
plot_data <- datam %>%
  filter(type %in% c('sigmoid-tail', 'sigmoid-right')) %>%
  filter(MCAR == '10')

bias <- plot_data %>%
  ggplot(aes(x = MNAR, y = bias, alpha = MAR, fill = type)) + 
  geom_bar(stat = "identity", position = position_dodge(), colour='black') + 
  labs(title = 'Mean shift') + 
  xlab('MNAR') + 
  ylab('') +
  guides(fill = guide_legend(direction = "horizontal")) +
  theme(legend.position="top",
        legend.justification="right",
        plot.title = element_text(vjust=-4), 
        legend.box.margin = margin(-1,0,0,0, "line"),
        #axis.title.y = element_text(),
        #panel.grid.major.x = element_blank(),
        #panel.grid.minor.x = element_blank(),
        #panel.grid.major.y = element_blank(),
        #panel.grid.minor.y = element_blank()
        ) + 
  scale_fill_manual(values=c("#fdb863", "#b2abd2"))

bias

name <- 'bias-combined.pdf'
ggsave(name, width = 20, height = 12, units = "cm")

# combination std
plot_data <- datam %>%
  filter(type %in% c('sigmoid-mid', 'sigmoid-left')) %>%
  filter(MCAR == '10')

std <- plot_data %>%
  ggplot(aes(x = MNAR, y = bias_std, alpha = MAR, fill = type)) + 
  geom_bar(stat = "identity", position = position_dodge(), colour='black') + 
  labs(title = 'Standard deviation shift') + 
  xlab('MNAR') + 
  ylab('') +
  guides(fill = guide_legend(direction = "horizontal")) +
  theme(legend.position="top",
        legend.justification="right",
        plot.title = element_text(vjust=-4), 
        legend.box.margin = margin(-1,0,0,0, "line"),
        #axis.title.y = element_text(),
        #panel.grid.major.x = element_blank(),
        #panel.grid.minor.x = element_blank(),
        #panel.grid.major.y = element_blank(),
        #panel.grid.minor.y = element_blank())
        )+ 
  scale_fill_manual(values=c("#fdb863","#b2abd2")) + 
  scale_y_continuous(limits = c(-0.00025, 0.0015))

std

name <- 'std-combined.pdf'
#name <- paste('std-', stype, '.eps', sep = "", collapse = NULL)
ggsave(name, width = 20, height = 12, units = "cm")

### plots for accuracy with bias ###

types <- c('sigmoid-right', 'sigmoid-left', 'sigmoid-tail', 'sigmoid-mid')
for(i in 1:length(types)){
  stype <- types[i]
  
  plot_data <- datam %>%
    filter(type == stype) %>%
    filter(MCAR == '0')

  acca <- plot_data %>%
    ggplot(aes(x=accuracy_a, y=bias, color=MAR, shape=MNAR)) +
      geom_point(size = 3) + 
      geom_errorbarh(aes(xmin=accuracy_a - (std_accuracy_a/1000),
                        xmax=accuracy_a + (std_accuracy_a/1000))) + 
      geom_errorbar(aes(ymin=bias - (bias/1000),
                       ymax=bias + (bias/1000))) +
      labs(title = 'Relation between mean shift and accuracy type a') + 
      xlab('accuracy type a') + 
      ylab('') +
      guides(fill = guide_legend(direction = "horizontal")) +
      theme(legend.position="top",
          legend.justification="right",
          plot.title = element_text(vjust=-4), 
          legend.box.margin = margin(-1,0,0,0, "line"),
          #axis.title.y = element_text(),
          #panel.grid.major.x = element_blank(),
          #panel.grid.minor.x = element_blank(),
          #panel.grid.major.y = element_blank(),
          #panel.grid.minor.y = element_blank()
          ) + 
    scale_colour_manual(values = c("#e66101", "#92c5de", "#a6d96a")) + 
    scale_shape_manual(values=c(22,23,24)) 
  #+ scale_x_continuous(limits = c(0.9175,0.926))

  acca

  name <- paste('acca-', stype, '.pdf', sep = "", collapse = NULL)
  ggsave(name, width = 16, height = 12, units = "cm")
}

# type b

types <- c('sigmoid-right', 'sigmoid-left', 'sigmoid-tail', 'sigmoid-mid')
for(i in 1:length(types)){
  stype <- types[i]
  
  plot_data <- datam %>%
    filter(type == stype) %>%
    filter(MCAR == '0')
  
  acca <- plot_data %>%
    ggplot(aes(x=accuracy_b, y=bias, color=MAR, shape=MNAR)) +
    geom_point(size = 3) + 
    geom_errorbarh(aes(xmin=accuracy_b - (std_accuracy_b/1000),
                       xmax=accuracy_b + (std_accuracy_b/1000))) + 
    geom_errorbar(aes(ymin=bias - (bias/1000),
                      ymax=bias + (bias/1000))) +
    labs(title = 'Relation between mean shift and accuracy type b') + 
    xlab('accuracy type b') + 
    ylab('') +
    guides(fill = guide_legend(direction = "horizontal")) +
    theme(legend.position="top",
          legend.justification="right",
          plot.title = element_text(vjust=-4), 
          legend.box.margin = margin(-1,0,0,0, "line"),
          #axis.title.y = element_text(),
          #panel.grid.major.x = element_blank(),
          #panel.grid.minor.x = element_blank(),
          #panel.grid.major.y = element_blank(),
          #panel.grid.minor.y = element_blank()
    ) + 
    scale_colour_manual(values = c("#e66101", "#92c5de", "#a6d96a")) + 
    scale_shape_manual(values=c(22,23,24)) 
  #+ scale_x_continuous(limits = c(0.9175,0.926))
  
  accb
  
  name <- paste('accb-', stype, '.pdf', sep = "", collapse = NULL)
  ggsave(name, width = 16, height = 12, units = "cm")
}

values <- dataa %>%
  mutate(bias = abs(as.numeric(bias)),
         accuracy_a = as.numeric(accuracy_a),
         accuracy_b = as.numeric(accuracy_b),
         std = as.numeric(std)) %>%
  group_by(MCAR,MAR,MNAR,type) %>%
  summarize(abias = mean(bias),
            astd = mean(bias_std),
            n=n())

values

corsa <- dataa %>%
  mutate(bias = abs(as.numeric(bias)),
         accuracy_a = as.numeric(accuracy_a),
         accuracy_b = as.numeric(accuracy_b),
         bias_std = abs(as.numeric(bias_std))) %>%
  filter(MCAR == '0') %>%
  group_by(type) %>%
  summarize(corbiasa = cor(bias, accuracy_a), 
            corbiasb = cor(bias, accuracy_b),
            corstda = cor(bias_std, accuracy_a), 
            corstdb = cor(bias_std, accuracy_b),
            n=n()) %>%
  mutate(corbiasa_se = sqrt((1-corbiasa^2)/(n-2)),
         corbiasb_se = sqrt((1-corbiasb^2)/(n-2)),
         corstda_se = sqrt((1-corstda^2)/(n-2)),
         corstdb_se = sqrt((1-corstdb^2)/(n-2)))
corsa

corsb <- dataa %>%
  mutate(bias = as.numeric(bias),
         accuracy_a = as.numeric(accuracy_a),
         accuracy_b = as.numeric(accuracy_b),
         bias_std = as.numeric(bias_std)) %>%
  filter(MCAR == '0') %>%
  group_by(type) %>%
  summarize(corbiasa = cor(bias, accuracy_a), 
            corbiasb = cor(bias, accuracy_b),
            corstda = cor(bias_std, accuracy_a), 
            corstdb = cor(bias_std, accuracy_b),
            n=n()) %>%
  mutate(corbiasa_se = sqrt((1-corbiasa^2)/(n-2)),
         corbiasb_se = sqrt((1-corbiasb^2)/(n-2)),
         corstda_se = sqrt((1-corstda^2)/(n-2)),
         corstdb_se = sqrt((1-corstdb^2)/(n-2)))
corsb

pt(0.0145/0.011, df = 8000, lower.tail = FALSE)


