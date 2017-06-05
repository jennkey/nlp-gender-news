import feedparser

def main():
    feed = feedparser.parse('http://www.denverpost.com/web-feeds/')
    #print(feed)
    for entry in feed['entries']:
        print(entry)
        content = urlopen(entry['link']).read()
        print(content)


main()

