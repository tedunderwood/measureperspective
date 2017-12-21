measuring the divergence between models
=====================================

The goal here is to come up with a metric of similarity between models *trained on different data.* I plan to develop a metric by assuming that a good metric should correlate with the percentage of data in training set A also found in training set B. Ultimately I want to use this metric to assess distances between training sets that have *no* instances in common. But my working premise is that a good metric would show a smaller distance between training sets that overlap than those that don't, while remaining as unaffected as possible by extraneous differences (the size of the training set, regularization constants, mean accuracy of the two models, etc).

In particular, I'm going to start with a case where the negative class is the same in both models (a collection of science fiction). I'm going to train a model of fantasy fiction against that contrast set, and then gradually adulterate the fantasy with randomly-selected volumes of mainstream fiction, which will differ from fantasy in a way quite different from the way science fiction differs.

Models will be trained that are 0% mainstream, 10% mainstream, etc. all the way to 100% mainstream. At each percentage level, we'll also try three different sizes (40 vols, 80 vols, 120 vols). All of these models will be trained using regularized logistic regression, optimized via a gridsearch on regularization coefficient and number of features.

This will create 30 models. For each of those models, we'll then measure the distance from 6 reference points:

* 40 vols, 0% mainstream
* 40 vols, 50% mainstream
* 40 vols, 100% mainstream
* 120 vols, 0% mainstream
* 120 vols, 50% mainstream
* 120 vols, 100% mainstream

In each case, distance will be measured by applying the test model to the same data used in the reference model, and vice-versa.  For each comparison, we'll record

* absolute difference in accuracy of the original model and the applied model
* Pearson's correlation between P(genre|text) produced by the two models
* Spearman correlation between P(genre|text) produced by the two models
* KL divergence between P(genre|text) produced by the two models

Correlations may need to pass through [the Fisher z-transformation.](https://en.wikipedia.org/wiki/Fisher_transformation) After that transformation, I'm hoping I can find a strong correlation between the absolute distance between two training sets (measured as percent mainstream) and the z-transformed correlation between the P(genre|text)s they produce. I'm also hoping this is commutative; i.e., one model's predictions about the other model's training set should be off by roughly as much as vice-versa.

Finally, I'm hoping that the correlation is not hugely distorted by differences in sample size. But I bet it is distorted! Probably we're going to learn that these comparisons only make sense if all models have roughly the same amount of data to work with. Probably we will also learn that the metric does not obey triangle inequality and is not really a distance.