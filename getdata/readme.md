code for scraping and munging data
==================================

**OCLC Classify Scrape** was used to get lists of volumes from [OCLC's experimental classification webservice](http://classify.oclc.org/classify2/). This notebook was originally developed in a project where Scott B. Weingart, Rikk Mulligan, Dan Evans, Matt Lavin, and Jessica Otis were the chief collaborators; I didn't write it.

**select_fantasy** and **select_sf** generate lists of volumes in those genres, partly by selecting volumes [from my HathiTrust fiction list](https://github.com/tedunderwood/noveltmmeta) that bear genre tags assigned by librarians, and partly by intersecting the HathiTrust list with an OCLC list of (mostly recent) volumes in those genres -- obtained from the **Classify Scrape** script above.

**fuse_old_and_new_fiction.py** concatenates two metadata sources to produce a list of all Hathi fiction

getting extracted features from HTRC
--------------------------------------

This part of the work is not reproducible in a push-button way, because I download extracted-feature files using an idiosyncratic workflow, and there's a better way for you to do it. If you want to add some additional files to the experiment, I actually recommend that you consult [the HTRC documentation](https://wiki.htrc.illinois.edu/display/COM/Extracted+Features+Dataset) and download files using their, simpler process. Then you can go to the next step, tokenization, where it becomes important that you use my scripts.

So this section of documentation is actually more for my benefit than the user's. However, if you're curious, here's how I do the downloading:

Once I've created metadata tables, I pass them to **generate_path_list**, which will harvest HathiTrust volume IDs from the metadata, in order to create simple summaries that I can use to download extracted-feature files from HTRC.

For instance, a command might be:

> python3 generate_path_list.py edited_random_fiction.csv merged_sff.csv supernatural.csv

That script (generate_path_list) requires a list of all-EF-paths that you are unlikely to have. That's why I recommend using [the HTRC process](https://wiki.htrc.illinois.edu/display/COM/Extracted+Features+Dataset) instead! But in any event, the point of the script is to concatenate the metadata files used as command-line arguments and create two metadata summaries: ids2pathlist.tsv and justpathlist.tsv. I can use the latter for downloading.

Then (in a directory where I store raw feature files) I do this command:

> rsync -a --files-from=/Users/tunder/Dropbox/python/pmla/getdata/justpathlist.txt data.analytics.hathitrust.org::features fic

That downloads extracted-features as a pairtree in the fic directory.

Then I can use the ids2pathlist.tsv as a metadata file to drive the next step of the process.

tokenization
-------------

This part of the workflow is reproducible, so you can add more files to the experiment if you like. The central script is **parsefeaturejsons.py**.

To run that script yourself, you need a few things:

First, a set of python modules and rule files located in this folder:

* SonicScrewdriver.py
* PersonalNames.txt
* PlaceNames.txt
* RomanNumerals.txt
* CorrectionRules.txt
* VariantSpellings.txt

Then, a metadata file mapping HathiTrust volume ids to paths where the extracted-feature file is available on your machine. (Should be a tsv with two columns, 'docid' and 'path.')

Finally, you'll need to hard-code the 'rootpath' in line 451 of parsefeaturejsons; this tells the script where to start, and the 'paths' listed in metadata are relative to the root.

If all that is available, the parsing script processes all the extracted features listed in metadata, and turns them into csvs. I've set things up so that it skips a few pages at the beginning and end of each volume. This is not a foolproof way of cutting paratext; in a perfect world I would trim it algorithmically or manually. I've also designed the script to divide large volumes into 2-4 parts; it tries to keep them in the range of 30,000 - 80,000 words, but there will be a few larger or smaller ones.
