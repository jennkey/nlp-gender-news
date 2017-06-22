# nlp-gender-news
NLP project to examine gender equity in newspapers across regions

UNDER CONSTRUCTION!!!!!!!

OVERVIEW

Media is both an influence and a reflection of our society.  The purpose of this project is to set up a process by which we can examine the representation of men and women in the news.  How often are each gender mentioned?  Are there certain topics that they are 'male' and others that are 'female'?  Do we see differences across regions?  What does this say about our society?

Analysis was done using Non-Negative Matrix Factorization (NMF) for extracting latent topics from the articles. Currently data is present from the Los Angeles Times, the Denver Post, the Atlanta Journal Constitution.

Future steps include pulling articles from more newspapers, including national syndicates.  Also looking at historical trends by pulling past  


The system


SIMILAR WORK

https://www.theverge.com/2013/5/10/4319386/gender-in-the-new-york-times-mapped-with-python-scripts
https://www1.udel.edu/comm245/readings/GenderedMedia.pdf
https://civic.mit.edu/blog/natematias/best-practices-for-ethical-gender-research-at-very-large-scales

CODE EXAMPLES

https://github.com/malev/gender-detector
http://nbviewer.jupyter.org/gist/nealcaren/5105037
https://github.com/bbengfort/gender-words-fatale

PROCESS

SCRAPE ARTICLES

CODE LOCATION: src/denpost, src/latimes, src/houston_chron, src/ajc



1) Set up process from data extraction into MongoDB, to topic modeling to gender detection on all articles,
   to results for Denver Post.
   a) Scrapy code - completed
   b) MongoDB feed - completed
   c) Topic Modeling -  completed
   d) Gender Detection - in progress
   e) results - not started

 2) Scrape articles for AJC - completed
 3) Scrape articles for LaTime - completed
