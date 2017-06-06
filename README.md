# nlp-gender-news
NLP project to examine gender equity in news across regions

OVERVIEW
On average women make 78 cents for every dollar a man earns.  One key factor that contributes to the wage gap is gender differences across occupations and industries.  Women represent only 26% of total employed in computers and mathematical occupations.    The question is why are more women so underrepresented in these high paying occupations.   I propose to examine one aspect of this question by looking at news media’s reporting on topics by gender.    Does the media paint an accurate picture of women in these professions?  How much of the reporting is devoted to discussing each gender?  For, example when technology is discussed in the news are women represented in a similar proportion to their representation in technology?  Using NLP I will examine the relationship between the media’s portrayal of women by ‘occupational topics’ by geographical region.  By looking across different regions in the country where the representation of women in key occupations is different I can examine the relationships between the devotion of each regional newspaper to each gender by occupational ‘topic’.  If the media is giving an accurate portrayal of females in key occupations then females should be mentioned in articles in the same proportion as their representation in each occupation.    
Since all content is not created equal, I will also examine if there are particular words or subjects that are more likely to be associated with articles devoted to females, such as ‘family’ and ‘work-life balance’ across all ‘occupational topics’.

SIMILAR WORK

https://www.theverge.com/2013/5/10/4319386/gender-in-the-new-york-times-mapped-with-python-scripts
https://www1.udel.edu/comm245/readings/GenderedMedia.pdf
https://civic.mit.edu/blog/natematias/best-practices-for-ethical-gender-research-at-very-large-scales

CODE EXAMPLES

https://github.com/malev/gender-detector
http://nbviewer.jupyter.org/gist/nealcaren/5105037
https://github.com/bbengfort/gender-words-fatale

PROCESS

1) Set up process from data extraction into MongoDB, to topic modeling to gender detection on all articles,
   to results for Denver Post.
   a) Scrapy code - X
   b) MongoDB feed - completed
   c) Topic Modeling - in progress
   d) Gender Detection - in progress
   e) results - not started

 2) Scrape articles for AJC,
