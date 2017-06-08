from pymongo import MongoClient
import pymongo
import pprint
client = MongoClient()

db = client.tryindex
#db['tryindex'].create_index({"source": 'text', "title": 'text'}, unique=True)
db.tryindex.create_index([("source", pymongo.TEXT), ("title", pymongo.TEXT)], unique=True, name='my_index')
