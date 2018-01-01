lab notebook
=============

Describing experiments on different ways of measuring divergence between models.

In particular, it's necessary to keep track of different experiments labeled here as "iterations," which might not otherwise be self-explanatory.

Iterations 0-4 tried to calibrate model divergence using a comparison between three different classes, two mixed in varying ratios to create a positive class that was distinguished from a third. This did not produce results that were consistent enough to be interpreted. In retrospect, I shouldn't be surprised, because god only knows what behavior we should expect from that three-body problem!

So I wrote new code **../logistic/metaselector.dilute_positive_class(),** which allowed me to gradually dilute the positive class by adding examples of the *negative* class, till at the end (100% dilution), we're trying to train a model between two sets randomly selected from the same group.

**In iterations 5-7,** I used this to train models that distinguish science fiction from a random background. Each model had eighty instances of the positive and negative classes, though the positive class was progressively diluted. Volumes were drawn from the entire timeline of the experiment (1800-2009). It's a strong contrast, topping out at 92.5% accuracy. 

Note that iterations 5 and 6 each contain 20 models, but iteration 7 only one. The reason is that, when I rewrote from a 3-class to a 2-class formulation, I also decided to measure divergence *from the gold standard* of an undiluted model. In other words, we compare the 5% diluted, 10% diluted, etc models all back to the original 0% diluted model, not (as I had previously attempted) permuting them all with each other.

This produced clearer results, but also meant that I had fewer data points, so I decided to create a third undiluted model, to allow multiple touchstones, and (especially) multiple comparisons among the undiluted models.

The models themselves are trained by **../logistic/methodological_experiment.vary_sf_ratio_against_random()** Comparisons among the models are made by **../logistic/methodological_experiment.measure_sf_divergences()**, and stored in sf_divergences.tsv.

**In iterations 8-10,** I followed the same procedure, but trained models of *fantasy* against a negative class consituted by science fiction. These models are considerably less accurate, topping out at 77.5%. Models are trained by are trained by **../logistic/methodological_experiment.vary_fantasy_ratio_against_sf()**. The divergences between models are measured by are trained by **../logistic/methodological_experiment.measure_fsf_divergences()**, and stored in fsf_divergences.tsv.

**In iterations 11-13,** I trained models of fantasy against a negative class of random fiction. I used functions vary_fantasy_ratio_against_random() and measure_fantasy_divergences(), and the results are stored in fantasy_divergences.tsv.

December 31 - new experiment
----------------------------

So, I just have not been confident that the artificial data in my previous experiment gave me a good yardstick. Genres are not actually created by mixing in random volumes. We are comparing to a *different* standard, not strictly a *weaker* version of the same one. Worse, the possibility of sharing some of the exact same volumes gave me a misleading baseline; there were situations where model A could do a better job of predicting model B than model B did, because model B was crossvalidated against itself, and model A wasn't.

All problematic! So, new plan. I know detective fiction is pretty remote from both fantasy and science fiction. Let's use that distance as a calibration

I'll start by dividing both fantasy and random volumes 1800-1920 into two partitions, A and B. Gold standard models will be trained within A. Comparison models will come from B. No shared volumes between the two.

Then we'll gradually mutate the B fantasy volumes by mixing them with detective fiction, on a word by word basis. In each case we'll take a random fantasy volume and a random detective volume, and replace X% of the fantasy features with detective features. In words shared between vols, we'll just replace the count for X% of words; in words unique, we'll replace X% of unique fantasy words with X% of unique detective words (and counts)

For X% in 0, 5, 10, 15, 20, 30, 40, 50, 60, 70, 80, 85, 90, 95, 100.

On either end, there is a gold standard constructed with entirely different volumes (detective or fantasy) contrasted against a non-overlapping random set (partition A). It's important to compare this against partition B: 0 / 100, which are different models of detective or fantasy, still generically pure, but different non-overlapping volumes than our genre baseline. The difference between those models is what should count as zero generic distance: not a self-comparison to an overlapping random set.

We'll calculate the distance from gold standards *in both directions*; i.e, from fantasy and from detective fiction. Part of the problem I'm dealing with is that "distances" are not symmetric, and I hope this will clarify how much of an issue that is.

Then we train a model to estimate "distances" between genres in terms of the distance between fantasy and detective fiction.

January 1
----------

The above experiment worked pretty well. It's in **logistic/methodological_experiment.new_experiment()** and **.new_divergences()**; data preparation was accomplished by **mix_data.py** and **copyrandom.py** in **measuredivergences.** Analysis is taking place in **spacebetweengenres.ipynb**.

The upshot is, I am resigning myself to the fact that there is no measure guaranteed to be truly symmetric or linear in this space. A lot depends in reality on the fit between particular datasets, and that can vary from one genre or sample or another. However, lost accuracy seems to work in practice extremely well, across a number of different experiments with data generated in different ways.

I originally ran this experiment (iterations 0-2) using partition 2 to generate the mixed data and partition 1 to create gold standard models that could be compared to models of the mixed data. But I think it may really matter which partitions you use, so I am flipping them. To be super-rigorous I would randomize them repeatedly, and I might yet do that!