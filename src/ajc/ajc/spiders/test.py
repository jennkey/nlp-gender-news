from scrapy.spiders import BaseSpider
from scrapy.selector import HtmlXPathSelector
from ajc.items import AjcItem
from scrapy.loader import ItemLoader
from scrapy import spider
from scrapy import Selector
from scrapy.http import Request
import re

class MySpider(BaseSpider):
    name = "ajc"
    allowed_domains = ["newser.com/rss.aspx", "rss.newser.com/rss"]
    start_urls = ["http://www.newser.com/rss.aspx"]


    def __init__(self):
        self.section = 'none'

    def parse(self, response):
        #From main page grab each section and link to the section
        sections = response.xpath("//*[@class='rssTable']/tbody/tr/td/strong/text()").extract()
        sec_links = response.xpath("//*[@class='rssTable']/tbody/tr/td/a/text()").extract()
        regex = re.compile(r'\b[a-z]{4,}\b')
        sec_links = filter(lambda i: regex.search(i), sec_links)
        sec_links = sec_links[0:2]
        #Open each link
        for idx, sec_link in enumerate(sec_links):
            self.section = sections[idx]
            print self.section
            yield Request(url=sec_link, dont_filter=True, callback=self.parse_topic)

    def parse_topic(self, response):
        # For each link from main page need to click on each article link
        # This code gives me the links for each article
        article_links = response.xpath('//guid/text()').extract()
        for article_link in article_links[0:1]:
            #print("article before yield request.", article_link)
            yield Request(url=article_link, dont_filter=True, callback=self.parse_article)

    def parse_article(self, response, section):
        source = 'AJC'
        section = self.section
        title = response.xpath('//meta[@name="pubexchange:headline"]/@content').extract()
        pubdate = response.xpath('//meta[@property="article:published_time"]/@content').extract()
        article = response.xpath('//*[@class="storyParagraph"]/text()').extract()
        article = ''.join(article).replace('\n','').replace('\r','')
        print (source)
        print (section)
        print (title)
        print (pubdate)
        print (article)
