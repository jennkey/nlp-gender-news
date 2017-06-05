import time
import urllib2
from urllib2 import urlopen
import re
import cookielib, urllib2
from cookielib import CookieJar
import datetime
from bs4 import BeautifulSoup
import pdb
from pymongo import MongoClient

client = MongoClient()
database = client['capstone']
coll = database['test_news']



cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

def main():
    try:
        page = 'http://www.denverpost.com/web-feeds/'
        sourceCode = opener.open(page).read()

        try:
            topics = []
            titles = []
            articles = []
            links = re.findall(r'<td.*?<a.*?href="(.*?)".*?</a>.*?</td>',sourceCode)
            links = list(set(links))
            links = links[0:1]
            for link in links:
                the_link = str(link) + '?format=xml'
                r = urlopen(the_link).read()
                soup = BeautifulSoup(r)
                titles = soup.find_all('title')
                contents = soup.find_all('content:encoded')
            for content in contents:
                content.aside.clear()
                article = content.get_text().encode('utf-8')
                #articles.append(article)
                print(article)
            #topics.append(the_link)
            #titles.append(title)
        except Exception, e:
            print str(e)

    except Exception,e:
        print str(e)
    return topics, titles, articles

topics, titles,articles = main()
