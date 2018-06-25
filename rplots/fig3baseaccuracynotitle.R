library(ggplot2)
library(scales)

sf <- read.csv('~/Dropbox/python/pmla/results/sf_nojuv_periods.tsv', sep = '\t')
fantasy <- read.csv('~/Dropbox/python/pmla/results/fantasy_nojuv_periods.tsv', sep = '\t')
sf$genre <- rep('sf', length(sf$name))
fantasy$genre <- rep('fantasy', length(fantasy$name))
all <-rbind(sf, fantasy)
for (i in seq(length(all$accuracy))){
  all$accuracy[i] = all$accuracy[i] + runif(1, -0.015, 0.015)
}

p <- ggplot(all, aes(color = genre)) +
  geom_segment(data = all, aes(x = floor, y = accuracy, xend = ceiling, yend = accuracy), size = 1.8) +
  scale_color_manual(values = c('black', 'gray65'),
                     guide = guide_legend(reverse = TRUE)) +
  scale_y_continuous('accuracy', labels = percent) +
  scale_x_continuous('') + theme_bw() + 
  theme(text = element_text(size = 16, family = "Avenir Next Medium"), 
        panel.border = element_blank(),
        axis.line = element_line(color = 'black'),
        plot.title = element_text(margin = margin(b = 14), size = 16, lineheight = 1.1))

tiff("~/Dropbox/python/pmla/images/Fig3NoTitle.tiff", height = 6, width = 8, units = 'in', res=400)
plot(p)
dev.off()
plot(p)