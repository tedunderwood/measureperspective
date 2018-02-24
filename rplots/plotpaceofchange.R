library(ggplot2)
library(scales)

pace <- read.csv('~/Dropbox/python/pmla/results/meanpacefrominterpretpaceofchange.csv')
for (i in seq(10)) {
  pace[i, 2] = 1 - pace[i, 2] 
  if (pace[i, 2] < 0) pace[i, 2] = 0
}

p <- ggplot(pace, aes(x = date, y = pace)) +
  geom_line(color = 'gray60', lwd = 3) +
  scale_y_continuous('percentage change', labels = percent) +
  scale_x_continuous('', breaks = c(1900, 1920, 1940, 1960, 1980, 2000)) + theme_bw() + 
  ggtitle('Pace of change from one 20-year period of SF\nto the next, measured through mutual recognition') +
  theme(text = element_text(size = 18, family = "Avenir Next Medium"), 
        panel.border = element_blank(),
        axis.line = element_line(color = 'black'),
        plot.title = element_text(margin = margin(b = 14), size = 16, lineheight = 1.1))

tiff("~/Dropbox/python/pmla/images/paceofchange.tiff", height = 6, width = 8, units = 'in', res=400)
plot(p)
dev.off()
plot(p)