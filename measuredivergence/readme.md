measuring the divergence between models
=====================================

The goal here is to come up with a metric of similarity between models *trained on different data.* I plan to develop a metric by assuming that a good metric should correlate with the percentage of data in training set A also found in training set B. Ultimately I want to use this metric to assess distances between training sets that have *no* instances in common, and that are in fact modeling different genre boundaries.

current state of conclusions
----------------------------
I think the experiment is complete, at least for now -- unless, say, reviewers force me to rethink my assumptions. The conclusions I have reached are organized in [**spacebetweengenres.ipynb.**](https://github.com/tedunderwood/measureperspective/blob/master/measuredivergence/spacebetweengenres.ipynb)

The conclusion I came to: Train multiple models of each genre, and compare models based on non-overlapping samples of data. The most reliable model of divergence is to calculate correlation (say, Spearman correlation) between the P(genre|text) predictions made by model A on B's data, and vice-versa. Do this both within genres (on non-overlapping samples) and across genres. Then calculate:

    meanCrossCorrelation(A, B) / max(meanSelfCorrelation(A), meanSelfCorrelation(B))

That will give you a measure of similarity that tracks the known similarities between datasets very closely. Note that it is not actually a distance metric: A -> B is not the same as B -> A. We're averaging across both directions to come up with something useful for projects that may not yet be ready to think through the messy reality of asymmetry.

history of experiments
----------------------

I had a hard time figuring out how to design this experiment; a history of different attempts is recorded in labnotebook.md.

All of the experiments did produce a fairly strong correlation between 

* the known distance between datasets A and B, and 
* the accuracy lost when models of A are applied to B (and vice-versa). 

We would expect those things to correlate strongly, and they always do. But I wanted to know exactly how strongly, and I wanted to know whether I could expect the linear relationship to be roughly the same for different genres.

It was difficult to figure out how to design a comparison that would be genuinely analogous to the kind of difference I expect when I'm comparing genres. At first I thought I could "dilute" a model by mixing negative examples into the positive class. For instance, a model of detective fiction vs. random contrast set, and then one where 5% of positive (detective) examples are replaced by other random examples, and then one where 10% are replaced, etc.

This was relatively easy to run, but not a very realistic picture of the degrees of difference we actually encounter between genres. Genre B is rarely just a less-consistent version of genre A, closer to the negative (contrast) set.

So I built a more complicated experiment, where two different genres are being compared to a random contrast set. At each intermediate point between the genres, we create a new dataset, by creating new files where 5%, 10%, and so on of the *features* in genre A are mixed with 95%, 90%, and so on of the *features* in genre B. (We do replacement at the type level rather than with individual tokens, but I think this is acceptable, since different types are replaced for each data file.)

This experiment is contained in **logistic/methodological_experiment.new_experiment()** and **.new_divergences()**. Data prep is done especially by **mix_data.py,** in this folder.

In my original experiment I had measured divergence in four ways:

* absolute difference in accuracy of the original model and the applied model
* Pearson's correlation between P(genre|text) produced by the two models
* Spearman correlation between P(genre|text) produced by the two models
* KL divergence between P(genre|text) produced by the two models

Correlations passed through [the Fisher z-transformation.](https://en.wikipedia.org/wiki/Fisher_transformation) to render them linear.

But I rapidly found that KL divergence was never a very good measure, and that Pearson and Spearman correlation were so close that we really only needed one or the other. So my final version of the experiment compares Spearman to lost-accuracy.

[Analysis in **spacebetweengenres.ipynb**](https://github.com/tedunderwood/measureperspective/blob/master/measuredivergence/spacebetweengenres.ipynb) has convinced me that Spearman correlation on P(genre|text) produced by two models is the most robust measure. Specifically, the divergence between genres can be estimated by

    meanCrossCorrelation(A, B) / max(meanSelfCorrelation(A), meanSelfCorrelation(B))

To be clear, divergence between genres is not symmetric; A->B and B->A are usually different. I don't think this really a distance metric. But the measure described above seems to be a robust measure of divergence for the kind of problems I will actually encounter. Older analysis on an earlier experiment can be found in **modelsofdivergence.ipynb.**