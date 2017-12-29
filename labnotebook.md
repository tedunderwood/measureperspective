lab notebook
=============

For earlier stages of work, especially initial methodological experiments on measuring divergence between models, see **measuredivergence/labnotebook.md**.

For preregistered hypotheses, see [a frozen registration at OSF.](https://osf.io/5b72w/register/5771ca429ad5a1020de2872e)

This lab notebook begins after that registration.

December 29
------------

**children's literature**

Key stages of research are preserved [in **logistic/main_experiment.py.**](https://github.com/tedunderwood/measureperspective/blob/master/logistic/main_experiment.py)

I ran an initial comparison of SF versus fantasy, preserved [as **modeloutput/fantasyvsSF1.csv**.](https://github.com/tedunderwood/measureperspective/blob/master/modeloutput/fantasyvsSF1.csv) Casual inspection of the output, sorted by the probability column, revealed that fantasy was strongly identified with children's literature, and the most fantastic books were almost always those for youngest audiences.

[A survey of metadata](https://github.com/tedunderwood/measureperspective/blob/master/metadata/metadata_survey.ipynb) revealed that juvenile fiction was going to cluster so strongly in particular genres and periods that results might be difficult to interpret. So, although I was getting very interesting results in this first run, it seemed clear that I would need to label children's lit. I did this cautiously, using guidelines described in the metadata survey above. Volumes were not removed, but I made it possible to exclude them from the calculation.

**genre differentiation from the mainstream**

Initial experiments, recorded in **results/sf_nojuv_periods** and results/fantasy_nojuv_periods,** reveal steady differentiation of fantasy and science fiction up to the 1980s, with a collapse thereafter, especially affecting SF.

**genre similarity: F/SF**

Had a lot of difficulty convincing myself that I was getting real data from this experiment.

As seen earlier in "The Life Cycles of Genre," direct classification of A against B becomes a crude measure of similarity when you're dealing with genres that are actually pretty similar. A classifier will always find some boundary, but it may not be a particularly stable one.

I think this is what we see in results/sf_vs_fantasy_periods. There's clearly some initial differentiation. Accuracy climbs from the low 70% range in the 19c toward 80% in the 20c. But the strength of the boundary is very volatile, and inspection of coefficients suggests that it may not be the same boundary in every period. Further research -- applying models cross-period -- might confirm.

Instead it has been more fruitful to ask whether A (sf) differs from (C) random mainstream fiction in the same way B (fantasy) does. And yes, models of A/C turn out to predict B/C extremely well and vice-versa. Average loss of accuracy is quite low -- in the single digits. In the past, I have tended to treat these kinds of results as evidence that two genres are effectively the same.

Getting a stable metric for this kind of cross-model comparison is still a bit of a beast. The problem I was having yesterday was, comparisons between random samples gave me an untrustworthy baseline, since the samples can contain a lot of shared volumes from one random pass to the next.

So this morning I decided to bite the bullet and write some bloody complex code preserved in main_experiment as quixotic_dead_end().

As you can see, I was not optimistic about success. But I think it is actually working. The strategy is to take large chunks of time, divide them randomly into two sets of volumes 1, 2 (with fantasy and sf ad well as the random vols partitioned). Then model A/C and B/C *within each partition only*. Then compare A/C(1) to A/C(2), B/C(1) to B/C(2), and A/C(1) to B/C(2) as well as A/C(2) to B/C(1) !!!

Coherence of these results with earlier dubious results achieved via less cautious methods has me somewhat convinced that there is a real pattern: fantasy and SF differentiate from each other through about the 1930s, remain quite distinct in the middle of the 20c, and then start to fuse in the 1990s, largely because *SF* is no longer as insistent about something that it was very obsessed with 1930-1980 (technology, science, space, testosterone, I'm not sure what to call it yet).

That's the state of play right now. Agenda for tomorrow is to run all these tests with more iterations so I have better measures of uncertainty.
