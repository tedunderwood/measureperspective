this.dir <- dirname(parent.frame(2)$ofile)
setwd(this.dir)

persp <- read.csv('data4r.csv')
library(ggplot2)
library(dplyr)
library(ggrepel)
tolabel <- persp[persp$label != '', ]

p <- ggplot(persp, aes(m, f)) + 
  theme_bw() +
  geom_point(alpha = 0.5) +
  scale_y_continuous('m   <--   in books by women  -->     f', limits = c(-15.5, 15.5)) +
  scale_x_continuous('m   <--   in books by men   -->    f', limits = c(-15.5, 15.5)) +
  geom_text_repel(aes(m, f, label = label), force = 6, box.padding = 0.3, 
                  point.padding = 0.8, max.iter = 1200, size = 4.2,
                  family = "Avenir Next Medium") +
  theme(text = element_text(size = 16, family = "Avenir Next Medium"), 
        panel.border = element_blank(),
        axis.line = element_line(color = 'black'),
        plot.title = element_text(margin = margin(b = 14), size = 16, lineheight = 1.1))

# annotate('text', x = -2.5 , y = -14.5, label = "Overrepresentation measured as\nthe signed log of Dunning's log-likelihood", 
# hjust = 0, family = 'Avenir Next Medium', size = 3.9)

tiff("fig1trial.tiff", height = 8, width = 8, units = 'in', res=400)
plot(p)
dev.off()
plot(p)