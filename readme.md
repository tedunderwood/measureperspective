A Measured Perspective
=========================

Code and data to support Ted Underwood, "A Measured Perspective."

There are four different sections of the article, but the first two draw on data from previous experiments; they will be lightly documented here, with links pointing out to other repositories.

The final two sections draw on new data, and will be completely documented in this repository.

[Section 1: Counting things](https://github.com/tedunderwood/measureperspective/tree/master/1counting)
==========================

Explains how figure 1 was produced. The raw data used for this figure is documented in [Chapter 4 of *Distant Horizons*](https://github.com/tedunderwood/horizon/tree/master/chapter4).

But intermediate stages of data, and the script that uses them to produce figure 1, are contained in the subfolder **1counting**.

[Section 2: Modeling perspectives](https://github.com/tedunderwood/measureperspective/tree/master/2modelingperspectives)
=================================

Contains code, and intermediate stages of data, used to produce figure 2. Again, the raw data is contained in another repository (it runs to several gigabytes). But intermediate stages of data and code are contained in the subfolder **2modelingperspectives**.

Sections 3 and 4: Comparing multiple perspectives, Measuring parallax
=====================================================================

These sections involve completely new samples of data and metadata. Instead of creating a separate folder for each section, I have spread the various components of the workflow across different folders (**/data**, **/metadata**, and so on) documented below.

The core question posed section 3 was, "Can we measure the differentiation of fictional genres?""
 I asked, in particular, whether fantasy and science fiction become more clearly distinct from mainstream fiction (and from each other) as we move down a timeline from the nineteenth century to the early twenty-first. (I owe the impulse to compare F and SF to a suggestion from Alan Liu.)

Part of a larger project about the measurement of "perspective" in literary history.

A [plan of research was pre-registered, Dec 24, 2017.](https://osf.io/5b72w/register/5771ca429ad5a1020de2872e)

Most data has been gathered and cleaned. The first substantive experiments have been run, with initial observations recorded in **labnotebook.md.** More experiments needed to assess uncertainty.

getdata
-------

Scripts I used to scrape genre tags, download data, and tokenize extracted features.

rawdata
-------

Early metadata files. It should really be named "rawmetadata" but the name is in too many scripts to change at this point.

mungedata
---------

All-purpose folder covering transformations of data and, especially, metadata.

logistic
--------

Code for predictive modeling. **main_experiment** and **methodological_experiment** in this folder are the heart of the project.

measuredivergence
-----------------

One of the challenges of this project is to figure out how we should measure the "distance" between predictive models. This task may not be quite as straightforward as it seems; e.g. I put scare quotes around *distance* because it's probably not literally a distance. I've reached a tentative conclusion, explained in [a Jupyter notebook **spacebetweengenres.**](https://github.com/tedunderwood/measureperspective/blob/master/measuredivergence/spacebetweengenres.ipynb)
