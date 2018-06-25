library(ggplot2)
library(scales)

fsf <- read.csv('~/Dropbox/python/pmla/results/groupedFSFdivergences.csv')

p <- ggplot(fsf, aes(x = dates, y = divergence)) +
  geom_point(shape = 18, size = 2, alpha = 0.5) + 
  geom_smooth(color = 'black', fill = 'gray70') +
  ylab('divergence') +
  scale_y_continuous(labels = percent, limits = c(0, 0.5)) +
  xlab('') + theme(text = element_text(size = 15)) +
  theme_bw() +
  theme(text = element_text(size = 16, family = "Avenir Next Medium"), 
        panel.border = element_blank(),
        axis.line = element_line(color = 'black'),
        plot.title = element_text(margin = margin(b = 14), size = 16, lineheight = 1.1))

tiff("~/Dropbox/python/pmla/images/Fig4wTitle.tiff", height = 6, width = 9, units = 'in', res=400)
plot(p)
dev.off()

plot(p)