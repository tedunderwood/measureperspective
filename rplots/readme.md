visualization scripts
=====================

My usual workflow is to manipulate data in Python, and then visualize it in R, using ggplot2. This repository includes the scripts that were used for the final stage of visualization, but in each case I have tried to provide some clue about the source of the data, so you can trace the figure back to the models that produced it.

Figure 1
--------

Was produced by **fig1authorship.R**, using data from **../1counting**.

Figure 2
---------

Was produced by **fig2perspectives.R**, using data from **../2modelingperspectives**.

Figure 3
---------

Was produced by **fig3baseaccuracy.R**. This draws immediately on two files in **../results/**, **sf_nojuv_periods.tsv** and **fantasy_nojuv_periods.tsv**. These, in turn, were created by **main_experiment.py**, in the **../logistic** directory, using the functions *sf_periods()* and *fantasy_periods()* in that script.

Figure 4
----------

Was produced by **fig4fsfcomparison.R**. This draws immediately on **../interpretations/groupedFSFdivergences.csv**, which is produced by **../interpretations/interpretFSFcomparison.ipynb**. That notebook, in turn, draws on data produced by the function *reliable_genre_comparisons()* in **../logistic/main_experiment.py**.

Figure 5
---------

Was produced by **fig5surprisearrows.R**. This draws immediately on **../results/sf1940_means.tsv**. For the process producing that data see **../surprise.**
