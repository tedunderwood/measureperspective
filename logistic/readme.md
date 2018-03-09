code for training predictive modelsin "A Measured Perspective"
==============================================================

This code is based on [predictive modeling code that has been kicking around](https://github.com/tedunderwood/horizon/tree/master/logistic) in my workflow for the last 2-3 articles.

But this version of the code has been refactored somewhat, to make better use of pandas. It's still going to be the most complex part of the workflow. But I think it's somewhat better documented, and easier to understand than it used to be.

If you want to reproduce models used in the article, you probably want to start with **main_experiment.py**. That script is what you would run to reproduce a particular model or group of models; in principle, all you need to know is what command to give it (see below).

Most of the other modules in this directory are resources called, directly or indirectly, by **main_experiment.py**. The exception is **methodological_experiment.py** which I used when testing different ways to measure the distance between genres; it is related to the work in **../measuredivergence.**

main_experiment
----------------

This is probably where you want to start exploring if you're trying to reproduce a particular model or set of models used in the article.

To run the module you enter

python3 main_experiment.py *command*

Where *command* is one of a number of options documented at the beginning of the main_experiment script.

versatiletrainer2
-----------------

This is really the core of the code in this folder; it contains a range of functions that guide the modeling process. Generally **main_experiment** calls **versatiletrainer2** with some parameters that define the particular sets of texts to be used in the positive and negative class of a model (dates, for instance, or genre labels).

metaselector
-------------

The actual selection of texts is usually outsourced to **metaselector**, which reads metadata and ensures, for instance, that positive and negative classes are distributed similarly across the timeline.

modelingprocess
---------------

Once volumes have been selected, features have been read, and everything has been converted into a numeric matrix, this module does the actual training of individual logistic models.

SonicScrewdriver
-----------------

I don't believe this module is actually used in the current version of the code! But I've left it in, because it often comes in handy.

