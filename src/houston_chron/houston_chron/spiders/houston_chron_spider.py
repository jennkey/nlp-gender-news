from scrapy.spiders import BaseSpider
from scrapy.selector import HtmlXPathSelector
from houston_chron.items import houston_chronItem
from scrapy.loader import ItemLoader
from scrapy import spider
from scrapy import Selector
from scrapy.http import Request
from string import punctuation
import re
from datetime import datetime, timedelta
from dateutil import parser


class MySpider(BaseSpider):
    name = "houston_chron"
    allowed_domains = ["chron.com"]
    start_urls = ["http://www.chron.com/rss"]

    def parse(self, response):
        subjects = response.xpath('//div[@class="itemWrapper"]//a/@href').extract()
        for subject in subjects:
            if subject.find("http") == -1:
                absolute_subject_url = 'http://www.chron.com' + subject
            else:
                absolute_subject_url = subject
            yield Request(url=absolute_subject_url, dont_filter=True, callback=self.parse_topic)

    def parse_topic(self, response):
        item = houston_chronItem()
        # get section and link
        section = response.xpath('//channel/title/text()').extract()
        sec_link = response.xpath('//channel/link/text()').extract()
        item['section'] = section
        # For each link from main page need to click on each article link
        # This code gives me the links for each article
        article_links = response.xpath('//item/link/text()').extract()
        pubDate_list = response.xpath('//item/pubDate/text()').extract()
        for idx, article_link in enumerate(article_links):
            #if parser.parse(pubDate_list[idx]) > (datetime.today() - timedelta(days=2)):
            item['pubdate'] = pubDate_list[idx]
            yield Request(url=article_link, dont_filter=True, callback=self.parse_article, meta={'item' : item})

    def parse_article(self, response):
        item = response.meta['item']
        source = 'houston_chron'
        title = response.xpath('//title/text()').extract()
        idx_title = [x.replace(' ','') for x in title]
        idx_title = [''.join(c for c in s if c not in punctuation) for s in idx_title]
        idx_title = [x.lower() for x in idx_title]
        article = response.xpath(".//*[@id='storyParagraphContainer']/p/text()").extract()
        #article = ''.join(article).replace('\n','').replace('\r','')
        item['idx_title'] = idx_title
        item['source'] = source
        item['title'] = title
        item['article'] = article
        yield item
