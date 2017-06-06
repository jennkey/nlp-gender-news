from pymongo import MongoClient
import pprint
client = MongoClient()

db = client.practice

articles = db.articles

aricles.count()
