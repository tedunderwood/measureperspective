surprise
========

Scripts that measure the difference between two perspectives at the level of individual words and pages in a novel.

Compare this to ../logistic/main_experiment.get_fantasy_surprise() and .get_rcc_surprise(), which generate lists of surprising books (stored in ../results)

These scripts, by contrast, are designed to take those measurements of parallax down to the level of individual pages and passages.

Tried several different ways of doing this. The options currently recommended are **create_surprise_metric** and **apply_normalized_surprise_metric.**

In contrast to some earlier versions, these scripts normalize model coefficients. In place of raw coefficients, we use the coefficient divided by the variance for that word, taken from the standard_scaler used in the model. This is important, because the coefficients otherwise overstate the effect of common words.
