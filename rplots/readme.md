visualization scripts
=====================

My usual workflow is to manipulate data in Python, and then visualize it in R, using ggplot2. This repository includes the scripts that were used for the final stage of visualization, but in each case I have tried to provide some clue about the source of the data, so you can trace the figure back to the models that produced it.

figure1.R
----------

Uses the ```ggrepel``` package to label points in figure 1, drawing data from **../genderedperspectives/data4r.csv.** For more information on how that table was produced, see the Jupyter notebook in the [**genderedperspectives** subfolder.](https://github.com/tedunderwood/measureperspective/tree/master/genderedperspectives)

figure2.R
---------

Draws immediately on two files in **../results/**, **sf_periods2.tsv** and **fantasy_periods2.tsv**.

These files summarize the accuracies of many modeling runs. They, in turn, were created by **main_experiment.py**, in the **../logistic** directory, using the functions ```sf_periods_2()``` and ```fantasy_periods_2()``` in that script.

The "periods2" suffix marks that these functions were run in AY 2018-19 as part of a revision that made modeling more precise.

figure3.R
----------

This draws immediately on **../interpretations/1940plotarrows.tsv**. The data was produced ultimately by the function ```get_rcc_surprise()``` in **../logistic/main_experiment.py**.

That function produces a number of files recording comparisons between two adjacent 30-year periods. The file **../results/sf1940_forward_surprises.tsv** is then filtered and arranged for visualization by **../interpretations/parallax.ipynb,** which writes the results out as **1940plotarrows.tsv.**
