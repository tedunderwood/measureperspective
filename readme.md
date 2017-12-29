A Measured Perspective
=========================

Can we measure the differentiation of fictional genres? We'll ask, in particular, whether fantasy and science fiction become more clearly distinct from mainstream fiction (and from each other) as we move down a timeline from the nineteenth century to the early twenty-first. (I owe the impulse to compare F and SF to a suggestion from Alan Liu.)

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

Code for predictive modeling.

measuredivergence
-----------------

One of the challenges of this project is to figure out how we should measure the "distance" between predictive models. This task may not be quite as straightforward as it seems; e.g. I put scare quotes around *distance* because it's probably not literally a distance. The only experiments I have run so far are general methodological experiments trying to calibrate a metric.