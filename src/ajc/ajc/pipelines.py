# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import pymongo
from scrapy.conf import settings

class MongoDBPipeline(object):
    def __init__(self):
        connection = MongoClient(
                settings['MONGODB_SERVER'],
                settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]
        #self.collection.create_index([("title", pymongo.TEXT)],unique=True, name='my_index')

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item
