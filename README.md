# Gender Representation in the News


## OVERVIEW

Media is both an influence and a reflection of our society.  The purpose of this project is to set up a process by which we can examine the representation of men and women in the news.  How often are each gender mentioned?  Are there certain topics that they are 'male' and others that are 'female'?  Do we see differences across regions?  What does this say about our society?


Analysis was done using article from three sources, Los Angeles Times, the Denver Post, the Atlanta Journal Constitution, covering June 5th to June 15th, 2017.  

Using Negative Matrix Factorization, topics were created across all sources for easier topic comparisons.  NMF yielded 60 topics.

To analyze gender, a process based on Neal Caren's work* was utilized.  Each sentence was categorized into one of four categories, male only, female only, male and female or none.  This was done by utilizing a list of gender-identifying words, such as 'he', 'she', 'him', 'her', etc.

Overall, across the 3 sources and all topics, there were 3.6 male sentences for every one female sentence.  Similar to what Caren found for the NYT, (3.2 male sentences for every 1 female sentence).

LA Times had the most mentions of men compared to women at 3.9 male sentences for every 1 female sentence.  While AJC had the fewest, with 3.1 male sentences for every 1 female sentence.



![results_by_source](images/readme/overall_source_ratio_map.png)

Topics that had the most mentions of men compared to women, were Sports and Politics.  While Education and Lifestyle were most gender balanced.  However, no topic mentioned females more often than males.

![main-topics-all-sources](images/readme/main-topics-all-sources.png)


Breaking down the sources by topics gives us the best indication of why the LA Times had the highest male to female sentence ratio and AJC the lowest.  Articles covering Sports had 10 male sentences for every 1 female sentence.  While AJC had fewer than 4 male sentences for every 1 female sentence.  

![main-topics-by-source](images/readme/main-topics-by-source.png)

Finally, just narrowing in on one of the main topics, politics, we can gain some insight into what is driving these numbers.  U.S. Politics is references men 5.1 times more often than women, consistent across all sources.  However, Local Politics is much more gender equal, in particular for AJC and The Denver Post.

![politics-by-source](images/readme/politics-by-source.png)







The system


References

*https://www.theverge.com/2013/5/10/4319386/gender-in-the-new-york-times-mapped-with-python-scripts
*https://www1.udel.edu/comm245/readings/GenderedMedia.pdf
*https://civic.mit.edu/blog/natematias/best-practices-for-ethical-gender-research-at-very-large-scales

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
