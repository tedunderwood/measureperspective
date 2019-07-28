this.dir <- dirname(parent.frame(2)$ofile)
setwd(this.dir)

library(ggplot2)
library(scales)

sf <- read.csv('../results/sf_periods2.tsv', sep = '\t')
fantasy <- read.csv('../results/fantasy_periods2.tsv', sep = '\t')
sf$genre <- rep('sf', length(sf$name))
fantasy$genre <- rep('fantasy', length(fantasy$name))
all <-rbind(sf, fantasy)
for (i in seq(length(all$accuracy))){
  all$accuracy[i] = all$accuracy[i] + runif(1, -0.01, 0.01)
  all$meandate[i] = all$meandate[i] + runif(1, -0.5, 0.5)
}

p <- ggplot(all, aes(color = genre, shape = genre)) +
  geom_point(data = all, aes(x = meandate, y = accuracy), size = 1.8) +
  geom_smooth(data = all, aes(x = meandate, y = accuracy), se = FALSE, size = 1.8, span = 0.5) +
  scale_color_manual(values = c('black', 'gray65'),
                     guide = guide_legend(reverse = TRUE)) +
  scale_shape_manual(values = c(16, 17),
                     guide = 'none') +
  scale_y_continuous('', labels = percent) +
  scale_x_continuous('') + theme_bw() + 
  theme(text = element_text(size = 16, family = "Avenir Next Medium"), 
        panel.border = element_blank(),
        axis.line = element_line(color = 'black'),
        plot.title = element_text(margin = margin(b = 14), size = 16, lineheight = 1.1),
        legend.title = element_blank())

tiff("~/Dropbox/python/pmla/images/figure2.tiff", height = 6, width = 8, units = 'in', res=400)
plot(p)
dev.off()
plot(p)