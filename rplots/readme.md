visualization scripts
=====================

My usual workflow is to manipulate data in Python, and then visualize it in R, using ggplot2. This repository includes the scripts that were used for the final stage of visualization, but in each case I have tried to provide some clue about the source of the data, so you can trace the figure back to the models that produced it.

Figure 3
---------

Was produced by **plotbaseaccuracy.R**. This draws immediately on two files in **../results/**, **sf_nojuv_periods.tsv** and **fantasy_nojuv_periods.tsv**. These, in turn, were created by **main_experiment.py**, in the **../logistic** directory, using the functions *sf_periods()* and *fantasy_periods()* in that script.

Figure 4
----------

Was produced by **FSFcomparison.R**. This draws immediately on **../results/groupedFSFdivergences.csv**, which is produced by **../results/interpretFSFcomparison.ipynb**. That notebook, in turn, draws on data produced by the function *reliable_genre_comparisons()* in **../logistic/main_experiment.py**.

NB *this function needs better documentation in the main_experiment script.*

Figure 5
---------

