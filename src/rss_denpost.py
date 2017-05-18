import time
import urllib2
from urllib2 import urlopen
import re
import cookielib, urllib2
from cookielib import CookieJar
import datetime
from bs4 import BeautifulSoup

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
            for link in links:
                the_link = str(link) + '?format=xml'
                r = urlopen(the_link).read()
                soup = BeautifulSoup(r)
                title = soup.find_all('title')
                content = soup.find_all('content:encoded')
                content[0].aside.clear()
                article = content[0].get_text()
                #print(the_link)
                topics.append[the_link]
                titles.append[title]
                articles.append[article] 
                #content[0].get_text()
                #article = content[0]
        #return topics, titles, articles 
        except Exception, e:
            print str(e)

    except Exception,e:
        print str(e)
        pass

main()
