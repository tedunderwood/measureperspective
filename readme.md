Machine Learning and Human Perspective
======================================

[![DOI](https://zenodo.org/badge/114384746.svg)](https://zenodo.org/badge/latestdoi/114384746)

Code and data to support Ted Underwood, "Machine Learning and Human Perspective," accepted for publication in PMLA.

The repository has been organized to document particular figures and assertions in the article.

[Section 1: From measurement to modeling](https://github.com/tedunderwood/measureperspective/tree/master/genderedperspectives)
=======================================

The subdirectory [**genderedperspectives/**](https://github.com/tedunderwood/measureperspective/tree/master/genderedperspectives) contains code, and intermediate stages of data, used to produce figure 1. The raw data is contained in another repository (it runs to several gigabytes).

Section 2: Multiplying perspectives and 3: Measuring parallax
=============================================================

These two sections of the article use shared sources of data and some shared code.

So instead of creating a separate folder for each section, I have spread the various components of the workflow across different folders (**data/**, **metadata/**, and so on) documented below.

If you're interested in understanding the immediate sources of evidence for a particular figure in the article, I would start with [**rplots/**,](https://github.com/tedunderwood/measureperspective/tree/master/rplots) which contains the R scripts actually used for visualization.

The paper trails for many passing assertions in the article--e.g., briefly cited accuracy figures--lead through the [**interpretations/** subfolder](https://github.com/tedunderwood/measureperspective/tree/master/interpretations). For instance, arguments about the increasing blurriness of the boundary between science fiction and fantasy are documented here.

Note that several notebooks in the **interpretations** folder are using more a rigorous measurement of the distance between two models than I had time to explain in the article. For full explanation of this more rigorous metric, see ["The Historical Significance of Textual Distances"](https://aclweb.org/anthology/papers/W/W18/W18-4507/) and/or the experiment documented in [**measuredivergence/**](https://github.com/tedunderwood/measureperspective/tree/master/measuredivergence).

To fully reproduce the predictive modeling in the article, you will need word counts for volume parts. I store these in a folder called simply **data**, but that folder is a little large for a github repo, so I am instead providing a link that allows download: [**DataForMeasuredPerspective.zip**](https://www.ideals.illinois.edu/handle/2142/99573).

If you want to replicate the research process from the beginning--and perhaps develop your own independent sample--I would recommend starting with [**rawdata/**,](https://github.com/tedunderwood/measureperspective/tree/master/rawdata) where I document the process of selecting the sample of books I used.

[rplots](https://github.com/tedunderwood/measureperspective/tree/master/rplots)
-------------------

Scripts that actually produce the figures in the article. Each script is associated with a brief pointer to sources of data.

[getdata](https://github.com/tedunderwood/measureperspective/tree/master/getdata)
-------

Scripts I used to scrape genre tags, download data, and tokenize extracted features.

[rawdata](https://github.com/tedunderwood/measureperspective/tree/master/rawdata)
-------

Early metadata files. It should really be named "rawmetadata" but the name is in too many scripts to change at this point.

[mungedata](https://github.com/tedunderwood/measureperspective/tree/master/mungedata)
---------

All-purpose folder covering transformations of data and, especially, metadata.

[logistic](https://github.com/tedunderwood/measureperspective/tree/master/logistic)
--------

Code for predictive modeling. **main_experiment** and **methodological_experiment** in this folder are the heart of the project.

[modeloutput](https://github.com/tedunderwood/measureperspective/tree/master/modeloutput)
-----------------------

Files produced by individual modeling runs. Files that end simply ".csv" contain predictions about individual volumes; files that end ".coefs.csv" contain the coefficients attached to individual words, and can be used to get a sense of the words that matter for a particular genre in a particular period. Files that end ".pkl" are machine-readable versions of a model; see **logistic/versatiletrainer2.py** to understand the format.

[results](https://github.com/tedunderwood/measureperspective/tree/master/results)
------------

This folder mostly contains files that summarize results across multiple modeling runs.

[interpretations](https://github.com/tedunderwood/measureperspective/tree/master/interpretations)
-----------------

Several Jupyter notebooks that survey results, visualize them, and discuss them. These notebooks provide support for several assertions made in passing in the third and fourth section of the article.

[measuredivergence](https://github.com/tedunderwood/measureperspective/tree/master/measuredivergence)
-----------------

One of the challenges of this project is to figure out how we should measure the "distance" between predictive models. This task may not be quite as straightforward as it seems; e.g. I put scare quotes around *distance* because it's probably not literally a distance. I've reached a tentative conclusion, explained in [a Jupyter notebook **spacebetweengenres.**](https://github.com/tedunderwood/measureperspective/blob/master/measuredivergence/spacebetweengenres.ipynb)

[surprise](https://github.com/tedunderwood/measureperspective/tree/master/surprise)
-----------------------

These scripts are used to find passages in a book that are "surprising" to earlier models of a genre. They're used in the section of the article on "measuring parallax."
