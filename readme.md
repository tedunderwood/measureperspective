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

The core question posed in section 3 was, "Can we measure the differentiation of fictional genres?""
 I asked, in particular, whether fantasy and science fiction become more clearly distinct from mainstream fiction (and from each other) as we move down a timeline from the nineteenth century to the early twenty-first. (I owe the impulse to compare F and SF to a suggestion from Alan Liu.)

Early in the project a [plan of research was pre-registered, Dec 24, 2017.](https://osf.io/5b72w/register/5771ca429ad5a1020de2872e)

If you're interested in reproducing the research process from the beginning, I would recommend starting with **/rawdata**, where I document the process of selecting the sample of books I used.

If you're interested in understanding the immediate sources of evidence for a particular figure in the article, I would start with **/rplots**, which contains the R scripts actually used for visualization.

To reproduce the predictive modeling in the article, you will need word counts for volume parts. I store these in a folder called simply **data**, but the folder is a little large for a github repo, so I am instead providing a link that allows download: [**DataForMeasuredPerspective.zip**](https://www.dropbox.com/s/hs1wxyfqsddx4s4/DataForMeasuredPerspective.zip?dl=0). Right now that simply links to my Dropbox; I'll replace it with an archival version as we get closer to publication.

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

[measuredivergence](https://github.com/tedunderwood/measureperspective/tree/master/measuredivergence)
-----------------

One of the challenges of this project is to figure out how we should measure the "distance" between predictive models. This task may not be quite as straightforward as it seems; e.g. I put scare quotes around *distance* because it's probably not literally a distance. I've reached a tentative conclusion, explained in [a Jupyter notebook **spacebetweengenres.**](https://github.com/tedunderwood/measureperspective/blob/master/measuredivergence/spacebetweengenres.ipynb)

[surprise](https://github.com/tedunderwood/measureperspective/tree/master/surprise)
-----------------------

These scripts are used to find passages in a book that are "surprising" to earlier models of a genre. They're used in the section of the article on "measuring parallax."
