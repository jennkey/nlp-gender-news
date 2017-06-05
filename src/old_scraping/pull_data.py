import newspaper

cnn_paper = newspaper.build('http://www.cnn.com/')

for article in cnn_paper.articles:
    print(article.url)

for category in cnn_paper.category_urls():
    print(category)

article = cnn_paper.articles[0]

article.download()

article.html

article.parse()

article.text



