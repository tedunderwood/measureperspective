Section 2: Modeling Perspectives
=================================

Code used to generate figure 2, which explores the divergence of two different perspectives on gender.

The raw data on characters is drawn from ["The Transformation of Gender in English-Language Fiction",](http://culturalanalytics.org/2018/02/the-transformation-of-gender-in-english-language-fiction/) and can be downloaded from [the *Cultural Analytics* Dataverse for the article.](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/ZM2MAN) It's quite voluminous (several gigabytes) and won't fit easily in github.

But this directory does contain the summary data I used to produce figure 2 (**chartable.tsv.zip**), as well as the script (**create_character_table.py**) that derived it from the raw data.

The full sequence of steps is as follows:

1. From the CA Dataverse, get **character_table_18c19c.tsv** and **character_table_post1900.tsv**.

2. Run **create_character_table.py**, which will use those files along with the lexicon present in this directory, and the **filtered_fiction_metadata** present in the sibling **/metadata** directory. This will generate **chartable.tsv**. (Or you can just unzip the zipped version of **chartable.tsv**, and start with the next step, 3.)

3. Run **gendered_perspectives.ipynb**. This does all the interesting work of comparing word frequencies using Dunning's log likelihood, plotting two perspectives against each other, etc. It uses **chartable.tsv** as raw data, and produces **data4r.csv** as output. (Or, you can skip this step, if you're really only interested in visualization, and start with the next step, 4.)

4. Run **plot2perspectives.R**. It uses the data produced in step 2, and produces figure 2 as output: **fig2plot2perspectives.tiff**.
