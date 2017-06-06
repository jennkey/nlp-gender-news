from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from denpost.items import DenpostItem
from scrapy.loader import ItemLoader
from scrapy import spider
from scrapy import Selector
from scrapy.http import Request
from bs4 import BeautifulSoup



class MySpider(BaseSpider):
    name = "denpost"
    #allowed_domains = ["http://www.denverpost.com/web-feeds/", "http://feeds.denverpost.com/"]
    rotate_user_agent = True
    allowed_domains = ["denverpost.com/web-feeds/", "feeds.denverpost.com/"]
    start_urls = ["http://www.denverpost.com/web-feeds/"]


    def parse(self, response):
        links = response.xpath('//table/tr/td/a/text()').extract()
        #links = links[11:12]
        #yield { link : links }
        for link in links:
            yield Request(url=link, dont_filter=True, callback=self.parse_topic)

    def parse_topic(self, response):
        sel = Selector(response)
        sel.register_namespace('content', "http://purl.org/rss/1.0/modules/content/")
        title = sel.xpath('.//title/text()').extract()
        section = title[0:1]
        titles = title[2:len(title)]
        #for t in title:
        #    if "The Denver Post" not in t:
        #        titles.append(t)
        pubdate = sel.xpath('.//pubDate/text()').extract()
        raw_articles = sel.xpath('.//content:encoded/text()').extract()
        articles = []
        for article in raw_articles:
            this_article = []
            soup = BeautifulSoup(article)
            for p in soup.find_all('p'):
                line = p.text
                line = line.replace('<p>','').replace('</p>','')
                this_article.append(line)
            articles.append(this_article)
        #print("length of articles", len(articles))
        for idx in range(len(articles)):
            print("going through loop", idx)
            l = ItemLoader(DenpostItem(), response=response)
            l.add_value('source', "Denver Post")
            l.add_value('section', section)
            l.add_value('title', titles[idx])
            l.add_value('pubdate', pubdate[idx])
            l.add_value('article', articles[idx])
            yield l.load_item()
