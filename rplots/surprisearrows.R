library(scales)
l <- read.csv('~/Dropbox/python/pmla/results/sf1940_means.tsv', sep = '\t')

title = paste('Probability of being science fiction, as seen from\nvantage points in 1910-39 ', sprintf('\u2192'),  ' → 1940-69')

p <- ggplot() + 
  geom_segment(data = l, aes(x= firstpub, y = alien, xend= firstpub, yend= original, colour = colour), 
               arrow = arrow(length = unit(0.2, "cm")), size = 0.8) +
  scale_color_manual(values = c('black', 'gray65')) +
  scale_y_continuous('', labels = percent, breaks = c(0.4, 0.5,0.6,0.7,0.8), limits = c(0.34, 0.84)) + 
  ggtitle('Probability of being science fiction, as seen from\nvantage points in 1910-39     1940-69'
) + scale_x_continuous("") +
  theme_bw() +
  theme(text = element_text(size = 16, family = "Avenir Next Medium"), 
        panel.border = element_blank(), legend.position = "none",
        axis.line = element_line(color = 'black'),
        plot.title = element_text(margin = margin(b = 14), size = 16, lineheight = 1.1),
        plot.margin = margin(1, 1, 0.5, 0.5, "cm"))
tiff("~/Dropbox/python/pmla/images/surprisearrows.tiff", height = 6, width = 8, units = 'in', res=400)
plot(p)
dev.off()
plot(p)