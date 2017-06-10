from scrapy.spiders import BaseSpider
from scrapy.selector import HtmlXPathSelector
from ajc.items import AjcItem
from scrapy.loader import ItemLoader
from scrapy import spider
from scrapy import Selector
from scrapy.http import Request
import re
from string import punctuation
from datetime import datetime, timedelta
from dateutil import parser

class MySpider(BaseSpider):
    name = "ajc"
    allowed_domains = ["newser.com/rss.aspx", "rss.newser.com/rss"]
    start_urls = ["http://www.newser.com/rss.aspx"]


    def __init__(self):
        self.section = 'none'

    def parse(self, response):
        global item
        #From main page grab each section and link to the section
        item = AjcItem()
        sections = response.xpath("//*[@class='rssTable']/tbody/tr/td/strong/text()").extract()
        sec_links = response.xpath("//*[@class='rssTable']/tbody/tr/td/a/text()").extract()
        regex = re.compile(r'\b[a-z]{4,}\b')
        sec_links = filter(lambda i: regex.search(i), sec_links)
        #print(sec_links)
        #sec_links = sec_links[0:2]
        #Open each link
        for idx, sec_link in enumerate(sec_links):
            self.section = sections[idx]
            item['section'] = self.section
            yield Request(url=sec_link, dont_filter=True, callback=self.parse_topic)

    def parse_topic(self, response):
        item = AjcItem()
        # get section and link
        section = response.xpath('//channel/title/text()').extract()
        sec_link = response.xpath('//channel/link/text()').extract()
        item['section'] = section
        print()
        print ("This is section", section)
        print()
        # For each link from main page need to click on each article link
        # This code gives me the links for each article
        article_links = response.xpath('//item/link/text()').extract()
        pubDate_list = response.xpath('//item/pubDate/text()').extract()
        for idx, article_link in enumerate(article_links):
            if parser.parse(pubDate_list[idx]) > (datetime.today() - timedelta(days=2)):
                yield Request(url=article_link, dont_filter=True, callback=self.parse_article,
                    meta={'item' : item})

    def parse_article(self, response):
        item = response.meta['item']
        source = 'AJC'
        title = response.xpath('//meta[@name="pubexchange:headline"]/@content').extract()
        pubdate = response.xpath('//meta[@property="article:published_time"]/@content').extract()
        article = response.xpath('//*[@class="storyParagraph"]/text()').extract()
        article = ''.join(article).replace('\n','').replace('\r','')
        item['source'] = source
        item['title'] = title
        item['pubdate'] = pubdate
        item['article'] = article
        yield item
