from bs4 import BeautifulSoup
import requests
req =
requests.get('http://www.chron.com/news/houston-texas/texas/article/the-highest-paid-athletes-in-Texas-Rockets-Astros-11209275.php')
req
soup = BeautifulSoup(req.text, html_parser)
soup = BeautifulSoup(req.text, html_parse)
soup = BeautifulSoup(req.text, 'html_parser')
soup = BeautifulSoup(req.text, 'html.parser')
souo
soup
soup.find_all('p')
_.body
__.body()
p = soup.find_all('p')
p.body()
type(p)
len(p)
p[0]
p[1]
p[2]
p[18]
p[17]
p[7]
attrs={'class': 'byline'}
soup.find_all('p',attr...})
%hist
