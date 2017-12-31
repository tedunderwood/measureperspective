scripts for data munging
========================

"Munging" is rather a catchall term. I'm just trying to document some of the messier steps of organizing data and metadata. These scripts are not guaranteed to work in a pushbutton way; they *document* how I *gathered* data, but are not intended as a fully reproducible workflow.

If you're trying to *reproduce* the data-gathering stage of research, you're probably better advised just to *replicate* the whole project with a sample of your own. That will be a better and more rigorous test.

dedup2earliest
--------------

Winnows long lists of possible volumes (../rawdata/fantasy_instersection.csv and ../rawdata/sf_intersection.csv), discarding duplicates and retaining the earliest copy in order to produce deduped_fantasy and deduped_sf in the /rawdata folder.

Then I manually went through the deduped files and dated a lot of early volumes, producing edited_sf and edited_fantasy.

sample_recent
--------------

This script runs on the edited files, randomly sampling the period after 1950 to get it down to a manageable scale.

fuse_genres1
------------

Merges sf and fantasy to create ../rawdata/merged_sff.csv.

dedup_allfic_2earliest, sample_random_fic and supplement_random_fic
-------------------------------------------------------------------

These scripts were all used to create a "random" contrast set. "Random" of course is an aspiration rather than a description. What it means here is: I first deduplicated my Hathi fiction using the same algorithm I had used to dedup the fantasy and science fiction (finding the earliest vol with the same title). This produced a deduplicated list in /rawdata/deduped_all_fiction.csv.

Then I sampled that list to get volumes distributed across time so that there would always be more random vols in a given decade than the max of *either* fantasy or scifi in that decade. The goal is to never be short of contrast volumes.

However, I also excluded from this set, not only volumes already in **merged_sff**, but any volume that was tagged as "Fantasy" or "Science fiction." Then I manually edited the resulting list, dating things roughly to first publication, and getting rid of any vols that were

* not really fiction, or

* obviously fantasy / science fiction

This last criterion is a little tricky. It's a place where my personal judgment gets involved. But it only affected about 4-5 volumes out of ~400. 

Different kinds of contrast sets are imaginable; one could allow the contrast set to overlap with the genre sets, for instance. I didn't do that because I felt that overlap would register increases in the sheer size of fantasy & science fiction (they're more likely to be sampled randomly) rather than real *similarity* between that genre and the random set.

simple_author_dedup
-------------------

Nothing is really ever simple, but this is my effort to identify authors that have variant names. It produces an **author_translation_table** that can be used to standardize names; the ultimate goal is to make sure that we are appropriately holding out instances by author when we crossvalidate.