surprise
========

Scripts that measure the difference between two perspectives at the level of individual words and pages in a novel.

I tried different ways of doing this. The options currently recommended are **create_surprise_metric.py** and **apply_normalized_surprise_metric.py.**

The strategy is fairly crude; I start with models that distinguish science fiction from a random contrast set in a range of different periods. Multiple models have been trained in each period; they are saved in ../modeloutput and their file names begin with "rccsf." (I could have updated this part of the process to use newer models that begin with "sfsurprise," but I didn't.)

Then I create a measure of "divergence between periods" for individual words by comparing the average coefficient in models for one period to the average coefficient in models for another. The list of words and measures of divergence is stored in the /crudemetrics folder, and it is then "applied" to a text in /rawtexts.

In contrast to some earlier stabs I took at the problem, these scripts normalize model coefficients. In place of raw coefficients, we use the coefficient divided by the variance for that word, taken from the standard_scaler used in the model. This is important, because the coefficients otherwise overstate the effect of common words.

Contrast all this to ```../logistic/main_experiment.get_sf_surprise()```, which generates lists of surprising *books* (stored in ../results).
