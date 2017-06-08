import newspaper
from newspaper import news_pool
from newspaper import Config
from pymongo import MongoClient

client = MongoClient('localhost:27017')
db = client.newsarticles

config = Config()
config.MAX_KEYWORDS = 100
config.fetch_image=False
config.memoize_articles = False

denpost_paper = newspaper.build('http://www.denverpost.com/', memoize_articles=False,
                fetch_image=False)
gjsent_paper = newspaper.build('http://www.gjsentinel.com/', fetch_image=False,
               memoize_articles=False)
la_paper = newspaper.build('http://www.latimes.com/', memoize_articles=False,
               fetch_image=False)
ajc_paper = newspaper.build('http://www.ajc.com/',
               memoize_articles=False, fetch_image=False)
indstar_paper = newspaper.build('http://www.indystar.com/',
               memoize_articles=False, fetch_image=False)

print("AJC size: ", ajc_paper.size())
print("Indian size: ", indstar_paper.size())
print("LA size: ", la_paper.size())
print("gjsent size: ", gjsent_paper.size())
print("denpost_paper: ", denpost_paper.size())
# bloomberg = newspaper.build('https://www.bloomberg.com/businessweek',
#                memoize_articles=False, fetch_image=False)

papers = [ajc_paper, indstar_paper, la_paper, denpost_paper, gjsent_paper]
#news_pool.set(papers, threads_per_source=2)
#news_pool.join

for paper in papers:
    for article in paper.articles[0:5]:
         source = paper.brand
         article_url = article.url
         article.download()
         article.parse()
         title = article.title
         content = article.text
         pubdate = article.publish_date
         article.nlp()
         keywords = article.keywords

         db.articles.insert_one({'source' : source, 'article_url': article_url,
               'title': title, 'content': content, 'pubdate': pubdate, 'keywords' : keywords} )

         print {'source' : source, 'article_url': article_url, 'title': title, 'content': content, 'pubdate': pubdate,
                 'keywords' : keywords, 'date_pulled' : '06/07/2017'}
