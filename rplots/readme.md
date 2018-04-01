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

The obvious question you will have about this figure is, "what did he do with volumes that were tagged as both 'fantasy' and 'science fiction'?" The answer is that they were allowed to belong to both genres; no other solution seemed appropriate. So the trajectory at the end of figure 4 may be *partly* shaped quite simply by the number of volumes that are explicit generic cross-overs. But that can't be the whole story, because the trends don't neatly align.

Figure 5
---------

Was produced by **fig5surprisearrows.R**. This draws immediately on **../results/sf1940_means.tsv**. The data was produced ultimately by the function *get_rcc_surprise()* in **../logistic/main_experiment.py**. That function produced ../results/sf1940newsurprises.tsv, which was munged cosmetically for figure 5 by ../results/mungezscores.py. I'm not sure this final script did anything with z scores, really; I think it mostly formatted the data for display.
