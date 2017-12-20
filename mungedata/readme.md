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