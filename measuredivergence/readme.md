measuring the divergence between models
=====================================

The goal here is to come up with a metric of similarity between models *trained on different data.* I plan to develop a metric by assuming that a good metric should correlate with the percentage of data in training set A also found in training set B. Ultimately I want to use this metric to assess distances between training sets that have *no* instances in common, and that are in fact modeling different boundaries. But my working premise is that a good metric would show a smaller distance between training sets that overlap than those that don't, while remaining as unaffected as possible by extraneous differences (the size of the training set, regularization constants, mean accuracy of the two models, etc).

**Here's the approach I adopted:**

We don't start out knowing, in principle, which genres are more or less similar to each other, so it's hard to calibrate the space of similarity between models.

We do know, however, that a model asked to discriminate between two random samples of the same set will produce very little useful information. So we might reasonably use that to mark "zero" on our thermometer. Whatever boundary (A vs. B) we want to model, a model of an entirely random boundary should count as "not at all meaningfully similar to it."

Then we could calibrate the space between A vs. B and sheer randomness by gradually mixing B into A. For instance, we could start diluting A by replacing 5% of the A examples with examples of B. This will weaken our model; the A/B boundary will be less accurately traced. Then we replace 10% of the examples of A. Then 15%, and so on. By the time we're done, we have twenty models defining the space between A/B and a random boundary.

We can compare each of those models to a "gold standard" where the positive class (A) is entirely undiluted. We'll try different measures of divergence, and see which correlate most closely with known difference between the training sets:

* absolute difference in accuracy of the original model and the applied model
* Pearson's correlation between P(genre|text) produced by the two models
* Spearman correlation between P(genre|text) produced by the two models
* KL divergence between P(genre|text) produced by the two models

Correlations may need to pass through [the Fisher z-transformation.](https://en.wikipedia.org/wiki/Fisher_transformation) After that transformation, I'm hoping I can find a strong correlation between the absolute distance between two training sets (measured as percent mainstream) and the z-transformed correlation between the P(genre|text)s they produce. I'm also hoping this is commutative; i.e., one model's predictions about the other model's training set should be off by roughly as much as vice-versa.

Finally, I'm hoping that the correlation is not hugely distorted by differences in sample size. But I bet it is distorted! Probably we're going to learn that these comparisons only make sense if all models have roughly the same amount of data to work with. Probably we will also learn that the metric does not obey triangle inequality and is a "divergence" rather than a distance.