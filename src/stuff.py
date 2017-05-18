from bs4 import BeautifulSoup   
import urllib
r = urllib.urlopen('http://feeds.denverpost.com/dp-news-breaking?format=xml').read()
soup = BeautifulSoup(r)
soup.find_all('title')
soup.find_all('content:encoded')
content[0].aside.clear()    
content[0].get_text()
