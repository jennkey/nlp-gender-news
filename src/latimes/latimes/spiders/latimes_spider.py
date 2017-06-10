from scrapy.spiders import BaseSpider
from scrapy.selector import HtmlXPathSelector
from latimes.items import latimesItem
from scrapy.loader import ItemLoader
from scrapy import spider
from scrapy import Selector
from scrapy.http import Request
from string import punctuation
import re
from datetime import datetime, timedelta
from dateutil import parser


class MySpider(BaseSpider):
    name = "latimes"
    allowed_domains = ["latimes.com"]
    start_urls = ["http://www.latimes.com/local/la-los-angeles-times-rss-feeds-20140507-htmlstory.html"]

    def parse(self, response):
        #global item
        #From main page grab each section and link to the section
        #sec_links = response.xpath('//div[@class="trb_article_page_body"]//a/@href').extract()
        sections = [
             u'All',
             u'Local',
             u'Crime',
             u'Data & Maps',
             u'Education',
             u'Neighborhoods',
             u'Politics',
             u'Transportation',
             u'L.A. Now',
             u'PolitiCal',
             u'SoCal Moments',
             u'Angels',
             u'Clippers',
             u'Dodgers',
             u'Kings',
             u'Lakers',
             u'NFL',
             u'Ducks',
             u'UCLA',
             u'USC',
             u'Dodgers Now',
             u'Lakers Now',
             u'Sports Now',
             u'Varsity Insider',
             u'Arts',
             u'Book Festival',
             u'Books',
             u'Movies',
             u'Music',
             u'Television',
             u'The Envelope',
             u'Cotown',
             u'Culture Monster',
             u'Gossip',
             u'Hero Complex',
             u'Jacket Copy',
             u'Movies Now',
             u'Pop & Hiss',
             u'Show Tracker',
             u'Nation',
             u'Politics',
             u'Science',
             u'Nation Now',
             u'Politics Now',
             u'Science Now',
             u'Afghanistan',
             u'Africa',
             u'Americas',
             u'Asia',
             u'Europe',
             u'Middle East',
             u'World Now',
             u'Autos',
             u'Finance',
             u'Hot Property',
             u'Jobs',
             u'Real Estate',
             u'Company Town',
             u'Technology Now',
             u'Editorials',
             u'Endorsements',
             u'Op-Ed',
             u'Top of the Ticket',
             u'Opinion L.A.',
             u'Fashion',
             u'Food',
             u'Health',
             u'Home & Garden',
             u'All the Rage ',
             u'Daily Dish',
             u'California',
             u'Hawaii',
             u'Las Vegas',
             u'Mexico',
             u'Deals and News',
             u'Regions Map',
             u'Angeles Forest',
             u'Antelope Valley',
             u'Beach Cities',
             u'Central L.A.',
             u'Eastside',
             u'Harbor',
             u'North County',
             u'Northeast L.A.',
             u'Northwest County',
             u'Pomona Valley',
             u'San Fernando Valley',
             u'San Gabriel Valley',
             u'Santa Monica Mountains',
             u'South Bay',
             u'Southeast',
             u'Verdugos',
             u'South L.A.',
             u'Westside',
             u'Sports',
             u'Entertainment',
             u'Nation',
             u'World',
             u'Business',
             u'Opinions',
             u'Lifestyle',
             u'Travel']
        sec_links = [
             u'http://www.latimes.com/rss2.0.xml',
             u'http://www.latimes.com/local/rss2.0.xml',
             u'http://latimes.com/local/crime/rss2.0.xml',
             u'http://www.latimes.com/local/datadesk/rss2.0.xml',
             u'http://www.latimes.com/local/education/rss2.0.xml',
             u'http://www.latimes.com/local/neighborhoods/rss2.0.xml',
             u'http://www.latimes.com/local/politics/rss2.0.xml',
             u'http://www.latimes.com/local/transportation/rss2.0.xml',
             u'http://www.latimes.com/local/lanow/rss2.0.xml',
             u'http://www.latimes.com/local/political/rss2.0.xml',
             u'http://www.latimes.com/local/moments/rss2.0.xml',
             u'http://www.latimes.com/sports/angels/rss2.0.xml',
             u'http://www.latimes.com/sports/clippers/rss2.0.xml',
             u'http://www.latimes.com/sports/dodgers/rss2.0.xml',
             u'http://www.latimes.com/sports/kings/rss2.0.xml',
             u'http://www.latimes.com/sports/lakers/rss2.0.xml',
             u'http://www.latimes.com/sports/nfl/rss2.0.xml',
             u'http://www.latimes.com/sports/ducks/rss2.0.xml',
             u'http://www.latimes.com/sports/ucla/rss2.0.xml',
             u'http://www.latimes.com/sports/usc/rss2.0.xml',
             u'http://www.latimes.com/sports/dodgers/dodgersnow/rss2.0.xml',
             u'http://www.latimes.com/sports/lakers/lakersnow/rss2.0.xml',
             u'http://www.latimes.com/sports/sportsnow/rss2.0.xml',
             u'http://www.latimes.com/sports/varsity-times/rss2.0.xml',
             u'http://www.latimes.com/entertainment/arts/rss2.0.xml',
             u'http://www.latimes.com/books/festivalofbooks/rss2.0.xml',
             u'http://www.latimes.com/books/rss2.0.xml',
             u'http://www.latimes.com/entertainment/movies/rss2.0.xml',
             u'http://www.latimes.com/entertainment/music/rss2.0.xml',
             u'http://www.latimes.com/entertainment/tv/rss2.0.xml',
             u'http://www.latimes.com/entertainment/envelope/rss2.0.xml',
             u'http://www.latimes.com/entertainment/envelope/cotown/rss2.0.xml',
             u'http://www.latimes.com/entertainment/arts/culture/rss2.0.xml',
             u'http://www.latimes.com/entertainment/gossip/rss2.0.xml',
             u'http://herocomplex.latimes.com/feed/',
             u'http://www.latimes.com/books/jacketcopy/rss2.0.xml',
             u'http://www.latimes.com/entertainment/movies/moviesnow/rss2.0.xml',
             u'http://www.latimes.com/entertainment/music/posts/rss2.0.xml',
             u'http://www.latimes.com/entertainment/tv/showtracker/rss2.0.xml',
             u'http://www.latimes.com/nation/rss2.0.xml',
             u'http://www.latimes.com/nation/politics/rss2.0.xml',
             u'http://www.latimes.com/science/rss2.0.xml',
             u'http://www.latimes.com/nation/nationnow/rss2.0.xml',
             u'http://www.latimes.com/nation/politics/politicsnow/rss2.0.xml',
             u'http://www.latimes.com/science/sciencenow/rss2.0.xml',
             u'http://www.latimes.com/world/afghanistan-pakistan/rss2.0.xml',
             u'http://www.latimes.com/world/africa/rss2.0.xml',
             u'http://www.latimes.com/world/mexico-americas/rss2.0.xml',
             u'http://www.latimes.com/world/asia/rss2.0.xml',
             u'http://www.latimes.com/world/europe/rss2.0.xml',
             u'http://www.latimes.com/world/middleeast/rss2.0.xml',
             u'http://www.latimes.com/world/worldnow/rss2.0.xml',
             u'http://www.latimes.com/business/autos/rss2.0.xml',
             u'http://www.latimes.com/business/personalfinance/rss2.0.xml',
             u'http://www.latimes.com/business/realestate/hot-property/rss2.0.xml',
             u'http://www.latimes.com/business/jobs/rss2.0.xml',
             u'http://www.latimes.com/business/realestate/rss2.0.xml',
             u'http://www.latimes.com/entertainment/envelope/cotown/rss2.0.xml',
             u'http://www.latimes.com/business/technology/rss2.0.xml',
             u'http://www.latimes.com/opinion/editorials/rss2.0.xml',
             u'http://www.latimes.com/opinion/endorsements/rss2.0.xml',
             u'http://www.latimes.com/opinion/op-ed/rss2.0.xml',
             u'http://www.latimes.com/opinion/topoftheticket/rss2.0.xml',
             u'http://www.latimes.com/opinion/opinion-la/rss2.0.xml',
             u'http://www.latimes.com/fashion/rss2.0.xml',
             u'http://www.latimes.com/food/rss2.0.xml',
             u'http://www.latimes.com/health/rss2.0.xml',
             u'http://www.latimes.com/home/rss2.0.xml',
             u'http://www.latimes.com/fashion/alltherage/rss2.0.xml',
             u'http://www.latimes.com/food/dailydish/rss2.0.xml',
             u'http://www.latimes.com/travel/california/rss2.0.xml',
             u'http://www.latimes.com/travel/hawaii/rss2.0.xml',
             u'http://www.latimes.com/travel/lasvegas/rss2.0.xml',
             u'http://www.latimes.com/travel/mexico/rss2.0.xml',
             u'http://www.latimes.com/travel/deals/rss2.0.xml',
             u'http://www.latimes.com/local/neighborhoods/',
             u'http://www.latimes.com/local/angeles-forest/rss2.0.xml',
             u'http://www.latimes.com/local/antelope-valley/rss2.0.xml',
             u'http://www.latimes.com/local/beach-cities/rss2.0.xml',
             u'http://www.latimes.com/local/central-la/rss2.0.xml',
             u'http://www.latimes.com/local/eastside/rss2.0.xml',
             u'http://www.latimes.com/local/harbor/rss2.0.xml',
             u'http://www.latimes.com/local/north-county/rss2.0.xml',
             u'http://www.latimes.com/local/northeast-la/rss2.0.xml',
             u'http://www.latimes.com/local/northwest-county/rss2.0.xml',
             u'http://www.latimes.com/local/pomona-valley/rss2.0.xml',
             u'http://www.latimes.com/local/san-fernando-valley/rss2.0.xml',
             u'http://www.latimes.com/local/san-gabriel-valley/rss2.0.xml',
             u'http://www.latimes.com/local/santa-monica-mountains/rss2.0.xml',
             u'http://www.latimes.com/local/south-bay/rss2.0.xml',
             u'http://www.latimes.com/local/southeast/rss2.0.xml',
             u'http://www.latimes.com/local/verdugos/rss2.0.xml',
             u'http://www.latimes.com/local/south-la/rss2.0.xml',
             u'http://www.latimes.com/local/westside/rss2.0.xml',
             u'http://www.latimes.com/sports/rss2.0.xml',
             u'http://www.latimes.com/entertainment/rss2.0.xml',
             u'http://www.latimes.com/nation/rss2.0.xml',
             u'http://www.latimes.com/world/rss2.0.xml',
             u'http://www.latimes.com/business/rss2.0.xml',
             u'http://www.latimes.com/opinion/rss2.0.xml',
             u'http://www.latimes.com/style/rss2.0.xml',
             u'http://www.latimes.com/travel/rss2.0.xml',
          ]
        #Open each link
        for idx, sec_link in enumerate(sec_links):
            yield Request(url=sec_link, dont_filter=True, callback=self.parse_topic)

    def parse_topic(self, response):
        item = latimesItem()
        # get section and link
        section = response.xpath('//channel/title/text()').extract()
        sec_link = response.xpath('//channel/link/text()').extract()
        item['section'] = section
        print()
        print ("This is section", section)
        print()
        # For each link from main page need to click on each article link
        # This code gives me the links for each article
        article_links = response.xpath('//item/link/text()').extract()
        pubDate_list = response.xpath('//item/pubDate/text()').extract()
        for idx, article_link in enumerate(article_links):
            if parser.parse(pubDate_list[idx]) > (datetime.today() - timedelta(days=2)):
                yield Request(url=article_link, dont_filter=True, callback=self.parse_article,
                    meta={'item' : item})

    def parse_article(self, response):
        item = response.meta['item']
        source = 'latimes'
        title = response.xpath('//title/text()').extract()
        idx_title = [x.replace(' ','') for x in title]
        idx_title = [''.join(c for c in s if c not in punctuation) for s in idx_title]
        idx_title = [x.lower() for x in idx_title]
        pubdate = response.xpath('//meta[@name="date"]/@content').extract()
        article = response.xpath('//div[@class="trb_ar_page"]/p/text()').extract()
        article = ''.join(article).replace('\n','').replace('\r','')
        item['idx_title'] = idx_title
        item['source'] = source
        item['title'] = title
        item['pubdate'] = pubdate
        item['article'] = article
        yield item
