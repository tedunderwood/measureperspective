results
=======

Files summarizing model output. (The actual model files are in **../modeloutput**)

There's also an interpretive Jupyter notebook here that interprets the comparisons between fantasy and science fiction.

Typically we have a file of **models** produced during the initial modeling, and then a file of **comparisons** that report statistics from cross-model comparison.

interpretFSFcomparison.ipynb
----------------------------
The payoff of a lot of work, revealing some clear trends in generic similarity.

bailey_to_19cSF
---------------
JO Bailey applied to contemporaneous 19c SF. Nearly impossible to distinguish.

bailey_to_detective
-------------------
Quite remote. 32% loss in accuracy.

bailey_to_postwar
-----------------
Notice that typically there's an asymmetry. Easier to predict backward than forward. Is this just because the later models are more strongly differentiated and more accurate?

fantasy_nojuv_periods
---------------------
This should be used as a base measure of differentiation, not the original fantasy_periods, which were distorted by inclusion of children's lit.

quixotic_comparisons
--------------------
Early attempt at SF/fantasy differentiation.

reliable_comparisons
--------------------
Better version of SF/fantasy comparisons, with partitions split by author. Produced by ../logistic/main_experiment.reliable_genre_comparisons(). See the Jupyer notebook above for an interpretation.