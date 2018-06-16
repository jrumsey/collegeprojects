suppressWarnings(suppressMessages(library(ggplot2)))

# from: http://www.cookbook-r.com/Graphs/Plotting_means_and_error_bars_(ggplot2)/
## Gives count, mean, standard deviation, standard error of the mean, and confidence interval (default 95%).
##   data: a data frame.
##   measurevar: the name of a column that contains the variable to be summariezed
##   groupvars: a vector containing names of columns that contain grouping variables
##   na.rm: a boolean that indicates whether to ignore NA's
##   conf.interval: the percent range of the confidence interval (default is 95%)
summarySE <- function(data=NULL, measurevar, groupvars=NULL, na.rm=FALSE,
                      conf.interval=.95, .drop=TRUE) {
  suppressMessages(library(plyr))

  # New version of length which can handle NA's: if na.rm==T, don't count them
  length2 <- function (x, na.rm=FALSE) {
    if (na.rm) sum(!is.na(x))
    else       length(x)
  }

  # This does the summary. For each group's data frame, return a vector with
  # N, mean, and sd
  datac <- ddply(data, groupvars, .drop=.drop,
                 .fun = function(xx, col) {
                   c(N    = length2(xx[[col]], na.rm=na.rm),
                     mean = mean   (xx[[col]], na.rm=na.rm),
                     sd   = sd     (xx[[col]], na.rm=na.rm)
                   )
                 },
                 measurevar
  )

  # Rename the "mean" column
  datac <- rename(datac, c("mean" = measurevar))

  datac$se <- datac$sd / sqrt(datac$N)  # Calculate standard error of the mean

  # Confidence interval multiplier for standard error
  # Calculate t-statistic for confidence interval:
  # e.g., if conf.interval is .95, use .975 (above/below), and use df=N-1
  ciMult <- qt(conf.interval/2 + .5, datac$N-1)
  datac$ci <- datac$se * ciMult

  return(datac)
}


dc4imp <- read.csv("connect-four-improved-experiment.csv")
dc4impse <- summarySE(dc4imp, measurevar="pct_improvement", groupvars=c("moves"))
p <- ggplot(dc4impse, aes(x=moves, y=pct_improvement)) +
  geom_errorbar(aes(ymin=pct_improvement-se, ymax=pct_improvement+se), width=.1) +
  geom_line() +
  geom_point() +
  scale_x_continuous("Connect Four pre-established moves") +
  scale_y_continuous("% improvement")
ggsave("connect-four-improved-experiment.png", p, width=6, height=4, dpi=100)

imp_won_cnt = nrow(subset(dc4imp, improved_won==1))
imp_won_pct = 100.0 * imp_won_cnt / nrow(dc4imp)
print(sprintf("New strategy win percent (you want this > 50): %.2f%%", imp_won_pct))

print(sprintf("Average improvement in efficiency (you want this > 0): %.2f%%", mean(dc4imp$pct_improvement)))
tt <- t.test(dc4imp$alphabeta, dc4imp$improved, paired=T)
print(sprintf("p-value of efficiency differences (you want this < 0.05): %.2f", tt$p.value))
