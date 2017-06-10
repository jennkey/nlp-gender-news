# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DenpostItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    idx_title = scrapy.Field()
    source = scrapy.Field()
    section = scrapy.Field()
    title = scrapy.Field()
    pubdate = scrapy.Field()
    article = scrapy.Field()
