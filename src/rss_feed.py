import time
import urllib2
from urllib2 import urlopen
import re
import cookielib, urllib2
from cookielib import CookieJar
import datetime

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

pattern_title = re.compile(r'(<title>(.*?)</title>)')
pattern_link = re.compile(r'(<link>(.*?)</link>)')

def main():
    try:
        page = 'http://www.huffingtonpost.com/feeds/index.xml'
        sourceCode = opener.open(page).read()
        #print sourceCode

        try:
            for m in re.finditer(pattern_title,sourceCode): 
                for n in re.finditer(pattern_link, sourceCode):
                    print m.group(0), '*', n.group(0) 
        except Exception, e:
            print str(e)

    except Exception,e:
        print str(e)
        pass

main()
