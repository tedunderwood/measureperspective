library(scales)
library(ggplot2)
l <- read.csv('~/Dropbox/python/pmla/interpretations/1940plotarrows.tsv', sep = '\t')
lsubset = l[l$title == 'Player piano.',  ]
title = paste('Probability of being science fiction, as seen from\nvantage points in 1910-39      1940-69')
legend = data.frame(
  x = c(1942),
  y = c(.4),
  size = 9.5
)
legendseg = data.frame(
  x = 1942,
  y = 0.4,
  xend = 1942,
  yend = 0.301
)

p <- ggplot() + 
  geom_segment(data = l, aes(x= firstpub, y = unweightpremean, xend= firstpub, yend= unweightpostmean, colour = colour), 
               arrow = arrow(length = unit(0.2, "cm")), size = 0.8) +
  geom_point(data = lsubset, aes(x = firstpub, y = unweightpremean, size = (100 * prestd)), color = 'gray70', alpha = 0.2) +
  scale_radius(range = c(25, 38)) +
  geom_point(data = lsubset, aes(x = firstpub, y = unweightpostmean, size = (100 * poststd)), color = 'gray70', alpha = 0.2) +
  scale_color_manual(values = c('black', 'gray65')) +
  geom_point(data = legend, aes(x=x, y=y, size = size), color = 'gray70', alpha = 0.2) +
  geom_segment(data = legendseg, aes(x = x, y = y, xend = xend, yend = yend), colour = 'black') +
  scale_y_continuous('probability of being SF', labels = percent, breaks = c(0, 0.2, 0.4, 0.6, 0.8, 1), limits = c(0, 1.02)) + 
  scale_x_continuous("", limits = c(1939, 1971)) +
  theme_bw() + ggtitle(title) +
  theme(text = element_text(size = 16, family = "Avenir Next Medium"), 
        panel.border = element_blank(), legend.position = "none",
        axis.line = element_line(color = 'black'),
        axis.text = element_text(color = 'black'),
        panel.grid.minor = element_line(colour = "white"),
        plot.title = element_text(margin = margin(b = 14), size = 16, lineheight = 1.1),
        plot.margin = margin(1, 1, 0.5, 0.5, "cm"))
tiff("~/Dropbox/python/pmla/images/NewerFig3.tiff", height = 6, width = 8, units = 'in', res=400)
plot(p)
dev.off()
plot(p)