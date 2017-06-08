import numpy as np
import pandas as pd
import re
import pdb

from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
#from nltk.stem.wordnet import WordNetLemmatizer

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF as NMF_sklearn
from sklearn.decomposition import LatentDirichletAllocation

from pymongo import MongoClient

client = MongoClient('localhost:27017')
db = client.news


# function to read records from mongo db
def read():
    df = pd.DataFrame(list(db.articles.find()))
    return df

def clean_text(contents):
    # remove 'by author'
    contents = contents.str.replace(r"By[^,]*","")
    #lower case all text
    contents = contents.str.lower()
    # change contractions to their long form
    contents = contents.str.replace(r"what's", "what is ")
    contents = contents.str.replace(r"what's", "what is ")
    contents = contents.str.replace(r"\'s", " ")
    contents = contents.str.replace(r"\'ve", " have ")
    contents = contents.str.replace(r"can't", "cannot ")
    contents = contents.str.replace(r"n't", " not ")
    contents = contents.str.replace(r"i'm", "i am ")
    contents = contents.str.replace(r"\'re", " are ")
    contents = contents.str.replace(r"\'d", " would ")
    contents = contents.str.replace(r"\'ll", " will ")

    #remove punctuation
    contents = contents.str.replace(r"[^\w\s]", "")
    return contents


def build_text_vectorizer(contents, use_tfidf=True, use_stemmer=False, max_features=None):
    '''
    Build and return a **callable** for transforming text documents to vectors,
    as well as a vocabulary to map document-vector indices to words from the
    corpus. The vectorizer will be trained from the text documents in the
    `contents` argument. If `use_tfidf` is True, then the vectorizer will use
    the Tf-Idf algorithm, otherwise a Bag-of-Words vectorizer will be used.
    The text will be tokenized by words, and each word will be stemmed iff
    `use_stemmer` is True. If `max_features` is not None, then the vocabulary
    will be limited to the `max_features` most common words in the corpus.
    '''
    Vectorizer = TfidfVectorizer if use_tfidf else CountVectorizer
    tokenizer = RegexpTokenizer(r"[\w']+")
    stem = PorterStemmer().stem if use_stemmer else (lambda x: x)
    stop_set = set(stopwords.words('english'))

    # Closure over the tokenizer et al.
    def tokenize(text):
        tokens = tokenizer.tokenize(text)
        stems = [stem(token) for token in tokens if token not in stop_set]
        return stems


    vectorizer_model = TfidfVectorizer(tokenizer=tokenize, max_features=max_features)
    vectorizer_model.fit(contents)
    vocabulary = np.array(vectorizer_model.get_feature_names())

    # Closure over the vectorizer_model's transform method.
    def vectorizer(X):
        return vectorizer_model.transform(X).toarray()

    return vectorizer, vocabulary


def hand_label_topics(H, vocabulary):
    '''
    Print the most influential words of each latent topic, and prompt the user
    to label each topic. The user should use their humanness to figure out what
    each latent topic is capturing.
    '''
    hand_labels = []
    for i, row in enumerate(H):
        top_five = np.argsort(row)[::-1][:20]
        print 'topic', i
        print '-->', ' '.join(vocabulary[top_five])
        label = raw_input('please label this topic: ')
        hand_labels.append(label)
        print
    return hand_labels

def softmax(v, temperature=1.0):
    '''
    A heuristic to convert arbitrary positive values into probabilities.
    See: https://en.wikipedia.org/wiki/Softmax_function
    '''
    expv = np.exp(v / temperature)
    s = np.sum(expv)
    return expv / s

def analyze_article(article_index, contents, web_urls, W, hand_labels):
    '''
    Print an analysis of a single article, including the article text
    and a summary of which topics it represents. The topics are identified
    via the hand-labels which were assigned by the user.
    '''
    print web_urls[article_index]
    print contents[article_index]
    probs = softmax(W[article_index], temperature=0.01)
    for prob, label in zip(probs, hand_labels):
        print '--> {:.2f}% {}'.format(prob * 100, label)
    print


def label_articles():
    for topic in topics:
        topic_labels.append(hand_labels[topic])
    #Need to update the mongo db with the topic label_articles
    # may need to somehow have kept the id field here is some sample code
    db.Doc.update({"_id": b["_id"]}, {"$set": {"geolocCountry": myGeolocCountry}})


def main():
    '''
    Read the data from MongoDB.
    Use NMF to find latent topics.
    '''

    #Read data from MongoDB
    df = read()
    df['article'] = df['article'].apply(lambda x: ', '.join(x))
    contents = df['article']

    contents = clean_text(contents)

    # Build our text-to-vector vectorizer, then vectorize our corpus.
    vectorizer, vocabulary = build_text_vectorizer(contents, use_tfidf=True,
                                 use_stemmer=False,
                                 max_features=500)

    X = vectorizer(contents)

    nmf = NMF_sklearn(n_components=20, max_iter=150, random_state=12345, alpha=0.2)
    W = nmf.fit_transform(X)
    H = nmf.components_
    print 'reconstruction error:', nmf.reconstruction_err_

    # choose topic for each document
    topics = np.argmax(W, axis=1)

    # match up titles to topics



    n_features = 1000
    n_topics = 20
    n_top_words = 20
    print("Fitting LDA models with tf features,")
    lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=10,
                                learning_method='online',
                                learning_offset=50.,
                                random_state=0,
                                )
    lda.fit(X)
    W_lda = lda.transform(X)
    H_lda = nmf.components_

    # hand_labels = hand_label_topics(H, vocabulary)
    #
    # for i in rand_articles:
    #     analyze_article(i, contents, web_urls, W, hand_labels)

if __name__ == '__main__':
    main()
