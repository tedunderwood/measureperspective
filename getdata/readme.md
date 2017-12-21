code for scraping and munging data
==================================

**OCLC Classify Scrape** was used to get lists of volumes from OCLC's experimental classification webservice](http://classify.oclc.org/classify2/). This notebook was originally developed in a project where Scott B. Weingart, Rikk Mulligan, Dan Evans, Matt Lavin, and Jessica Otis were the chief collaborators; I didn't write it.

**select_fantasy** and **select_sf** generate lists of volumes in those genres, partly by selecting volumes [from my HathiTrust fiction list](https://github.com/tedunderwood/noveltmmeta) that bear genre tags assigned by librarians, and partly by intersecting the HathiTrust list with an OCLC list of (mostly recent) volumes in those genres -- obtained from the **Classify Scrape** script above.

**fuse_old_and_new_fiction.py** concatenates two metadata sources to produce a list of all Hathi fiction