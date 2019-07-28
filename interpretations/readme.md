interpretations
================

Mostly Jupyter notebooks that engage in initial exploratory visualization of patterns produced by **../logistic/main_experiment()**.

These notebooks document many passing assertions in the article.

In particular:

Questions about the strength of the boundary between fantasy and science fiction are answered in **interpretFSFcomparison.ipynb**. E.g., the figures 9-11% and 6% at the end of section 2, "Multiplying Perspectives." This notebook uses a file (../results/reliable_comparisons.tsv) that was produced by the function ```reliable_genre_comparisons()``` in ../logistic/main_experiment.py. *Note that the simplified section at the end of the notebook is the only part actually used in the article;* everything else is a more rigorous and complicated analysis that leads to roughly the same conclusion.

**interpretgenrecomparisons.ipynb** poses questions about loss of accuracy between Scarborough, Bailey, etc; it supports assertions made in passing in section 2 of the article.

**interpretpaceofchange.ipynb** poses questions about the pace of change in science fiction. It supports assertions made in passing in section 3, "Measuring parallax." (Note that these assertions also depend on other analysis, including analysis in chapter 2 of *Distant Horizons* (Univ of Chicago Press, 2019). This notebook uses a file, ..results/change_comparisons.tsv, which was produced by the function ```reliable_change_comparisons()``` in **../logistic/main_experiment.py.**

**genrespace.ipynb** is a dubious experiment not used in the article.

The name of this folder is not meant as an assertion about the hermeneutic character of the actions herein performed. It's just a name, y'all.




