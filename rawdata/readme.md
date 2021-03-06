raw data sources for "A Measured Perspective"
============================================================

The workflow here began with two different categories of metadata.

* First, a list of *books available,* -- basically, [all the English-language fiction I could find in HathiTrust.](https://github.com/tedunderwood/noveltmmeta) For a discussion of error in this list, follow the link to the repository where it is discussed.

* On the other hand, lists of volumes identified as belonging to specific genres by specific witnesses. These could be collective witnesses (librarians, OCLC), or specific bibliographies and scholarly works.

    - Some of the lists were drawn from [OCLC's experimental classification webservice](http://classify.oclc.org/classify2/), using code developed by Scott B. Weingart, Rikk Mulligan, Dan Evans, Matt Lavin, and Jessica Otis.

    - Others were based on Library of Congress genre/form classifications present in HathiTrust metadata.

    - Many other lists were drawn manually from specific bibliographies or studies of genre.

Lists that begin **oclc** come from the **Classify** webservice described above. Note that the format of these lists is not consistent; the science_fiction one is older, and was generated by Scott Weingart; the others are more recent and generated by me. They all have a strong bias toward works recently reprinted and tend to neglect older works if not reprinted. The all_fiction list is by no means really comprehensive; I used it only to abbreviate my manual labor, not as a source in itself.

winnowing and deduplicating
---------------------------

I created initial lists of fantasy and science fiction by running **../getdata/select_sf.py** and **../getdata/select_fantasy.py** These scripts create lists of Hathi vols that were either explicitly tagged sf/fantasy or that match the oclc (either through oclc id or through title/auth fuzzy matching).

The next stage is to deduplicate those lists, retaining only the earliest copy of each title. This was done by **../mungedata/dedup2earliest.py** The same script can run on both genres. Note that, in deduplicating, we retain info about the original reason(s) for inclusion of all examples of a title, so a title that was both tagged SF in Hathi and included in the OCLC list will retain tags for both "reasons."

Manual editing transformed the *deduped* files into the *edited* files. Mainly I was trying to identify date of first publication, to get a sense of how many vols per decade I had in the early going. I also removed some duplicates that slipped through the screen.

Once I knew how dense the data was before 1950, I ran **../mungedata/sample_recent.py** to downsample the post-1950 part of the dataset to a roughly equal, manageable size. This produced **chosen_fantasy.csv** and **chosen_sf.csv**.

bibliographies and critical sources
------------------------------------

I could rarely get all the works mentioned by a source. But I tried to get works (and especially authors) who are mentioned frequently or prominently.

**supernatural.csv** is drawn from [Dorothy Scarborough, *The Supernatural in Modern English Fiction* (1917).](https://catalog.hathitrust.org/Record/011213105) Scarborough's categories interestingly cut across genres we might separate out as fantasy, horror, and science fiction. She includes a chapter on "Supernatural Science," for instance, and sees H G Wells as an example. But Dunsany's style of fantasy and ghost stories are also included.
