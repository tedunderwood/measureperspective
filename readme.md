Machine Learning and Human Perspective
======================================

[![DOI](https://zenodo.org/badge/114384746.svg)](https://zenodo.org/badge/latestdoi/114384746)

Code and data to support Ted Underwood, "Machine Learning and Human Perspective," accepted for publication in PMLA.

The repository has been organized to document particular figures and assertions in the article. This readme file proceeds through the article and points to supporting code in each instance.

[Section 1: From measurement to modeling](https://github.com/tedunderwood/measureperspective/tree/master/modelingperspectives)
=======================================

The subdirectory [**modelingperspectives**](https://github.com/tedunderwood/measureperspective/tree/master/modelingperspectives) contains code, and intermediate stages of data, used to produce figure 1. The raw data is contained in another repository (it runs to several gigabytes).

Sections 3 and 4: Comparing multiple perspectives, Measuring parallax
=====================================================================

These sections involve completely new samples of data and metadata. Instead of creating a separate folder for each section, I have spread the various components of the workflow across different folders (**/data**, **/metadata**, and so on) documented below.

The core question posed in section 3 was, "Can we measure the differentiation of fictional genres?""
 I asked, in particular, whether fantasy and science fiction become more clearly distinct from mainstream fiction (and from each other) as we move down a timeline from the nineteenth century to the early twenty-first. (I owe the impulse to compare fantasy and science fiction to a suggestion from Alan Liu.)

Early in the project a [plan of research was pre-registered, Dec 24, 2017.](https://osf.io/5b72w/register/5771ca429ad5a1020de2872e)

If you're interested in reproducing the research process from the beginning, I would recommend starting with [**/rawdata**,](https://github.com/tedunderwood/measureperspective/tree/master/rawdata) where I document the process of selecting the sample of books I used.

If you're interested in understanding the immediate sources of evidence for a particular figure in the article, I would start with [**/rplots**,](https://github.com/tedunderwood/measureperspective/tree/master/rplots) which contains the R scripts actually used for visualization.

To reproduce the predictive modeling in the article, you will need word counts for volume parts. I store these in a folder called simply **data**, but that folder is a little large for a github repo, so I am instead providing a link that allows download: [**DataForMeasuredPerspective.zip**](https://www.ideals.illinois.edu/handle/2142/99573).

[rplots](https://github.com/tedunderwood/measureperspective/tree/master/rplots)
-------------------

Scripts that actually produce the figures in the article. If you're interested in retracing the process that produced a particular figure, it can be a good idea to start here; each figure is associated with a brief pointer to sources of data.

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
