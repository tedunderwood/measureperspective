lab notebook
=============

Describing experiments on different ways of measuring divergence between models.

In particular, it's necessary to keep track of different experiments labeled here as "iterations," which might not otherwise be self-explanatory.

Iterations 0-4 tried to calibrate model divergence using a comparison between three different classes, two mixed in varying ratios to create a positive class that was distinguished from a third. This did not produce results that were consistent enough to be interpreted. In retrospect, I shouldn't be surprised, because god only knows what behavior we should expect from that three-body problem!

So I wrote new code **../logistic/metaselector.dilute_positive_class(),** which allowed me to gradually dilute the positive class by adding examples of the *negative* class, till at the end (100% dilution), we're trying to train a model between two sets randomly selected from the same group.

**In iterations 5-7,** I used this to train models that distinguish science fiction from a random background. Each model had eighty instances of the positive and negative classes, though the positive class was progressively diluted. Volumes were drawn from the entire timeline of the experiment (1800-2009). It's a strong contrast, topping out at 92.5% accuracy. 

Note that iterations 5 and 6 each contain 20 models, but iteration 7 only one. The reason is that, when I rewrote from a 3-class to a 2-class formulation, I also decided to measure divergence *from the gold standard* of an undiluted model. In other words, we compare the 5% diluted, 10% diluted, etc models all back to the original 0% diluted model, not (as I had previously attempted) permuting them all with each other.

This produced clearer results, but also meant that I had fewer data points, so I decided to create a third undiluted model, to allow multiple touchstones, and (especially) multiple comparisons among the undiluted models.

The models themselves are trained by **../logistic/methodological_experiment.vary_sf_ratio_against_random()** Comparisons among the models are made by **../logistic/methodological_experiment.measure_sf_divergences()**, and stored in sfrandom_divergences.tsv.

**In iterations 8-10,** I followed the same procedure, but trained models of *fantasy* against a negative class consituted by science fiction. These models are considerably less accurate, topping out at 77.5%. Models are trained by are trained by **../logistic/methodological_experiment.vary_fantasy_ratio_against_sf()**. The divergences between models are measured by are trained by **../logistic/methodological_experiment.measure_fantasy_divergence_from_sf()**, and stored in fsf_divergences.tsv.


