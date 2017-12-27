library(scales)
library(ggplot2)
library(dplyr)

l <- read.csv('../modeloutput/fantasyvsSF2.csv')

l$reviewed <- as.factor(l$realclass)
levels(l$reviewed) = c('biography\n', 'fiction\n')

p <- ggplot(l, aes(x = std_date, y = probability, color = reviewed, shape = reviewed)) + 
  geom_point() + geom_smooth() + 
  scale_color_manual(name = 'actually\n', values = c('gray60', 'black'),
                     guide = guide_legend(keyheight = 3,  label.vjust = -0.4, override.aes = list(linetype = 0, fill = NA, size = 3))) + 
  theme(text = element_text(size = 24)) + scale_size(guide = FALSE, range = c(1.5,3.5)) +
  scale_y_continuous('', labels = percent) + 
  scale_x_continuous("") + theme_bw() +
  theme(text = element_text(size = 24, family = "Baskerville"), panel.border = element_blank()) +
  theme(axis.line = element_line(color = 'black'),
        axis.text = element_text(color = 'black')) +
  scale_shape_discrete(name = "actually\n")

tiff("/Users/tunder/Dropbox/book/chapter1/images/C1Fig4probabilities.tiff", height = 6, width = 9, units = 'in', res=400)
plot(p)
dev.off()
plot(p)