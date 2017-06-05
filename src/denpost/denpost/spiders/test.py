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
    allowed_domains = ["denverpost.com/web-feeds/", "feeds.denverpost.com/"]
    start_urls = ["http://www.denverpost.com/web-feeds/"]


    def parse(self, response):
        l = ItemLoader(DenpostItem(), response=response)
        links = response.xpath('//table/tr/td/a/text()').extract()
        links = links[0:1]
        #yield { link : links }
        for link in links:
            yield Request(url=link, dont_filter=True, callback=self.parse_topic)

    def parse_topic(self, response):
        l = ItemLoader(DenpostItem(), response=response)
        sel = Selector(response)
        sel.register_namespace('content', "http://purl.org/rss/1.0/modules/content/")
        #items = sel.xpath('//item').extract()
        #section = link 
        #print("this is the section", section)
        title = sel.xpath('.//title/text()').extract()
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
        print('****************************************')
        print("this is articles", articles)
            #for idx in xrange(0,len(title)):
                #l.add_value('source', "Denver Post")
                #l.add_value('section', section[idx])
                #l.add_value('title', title[idx])
                #l.add_value('pubdate', pubdate[idx])
               # l.add_value('article', article[idx])
               # return l.load_item()
        for article in articles:
            yield { 'article' : article}

