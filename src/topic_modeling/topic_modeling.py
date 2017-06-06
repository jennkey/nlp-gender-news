import numpy as np
import pandas as pd

from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF as NMF_sklearn

from pymongo import MongoClient

client = MongoClient('localhost:27017')
db = client.practice


# function to read records from mongo db
def read():
    df = pd.DataFrame(list(db.articles.find()))
    return df

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

    vectorizer_model = Vectorizer(tokenizer=tokenize, max_features=max_features)
    vectorizer_model.fit(contents)
    vocabulary = np.array(vectorizer_model.get_feature_names())


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




def main():
    '''
    Read the data from MongoDB.
    Use NMF to find latent topics.
    '''

    #Read data from MongoDB
    df = read()

    df['article'] = df['article'].apply(lambda x: ', '.join(x))

    contents = df['article']

    # Build our text-to-vector vectorizer, then vectorize our corpus.
    vectorizer, vocabulary = build_text_vectorizer(contents, use_tfidf=True,
                                 use_stemmer=False,
                                 max_features=5000)

    X = vectorizer(contents)

    nmf = NMF_sklearn(n_components=7, max_iter=100, random_state=12345, alpha=0.0)
    W = nmf.fit_transform(df['article'])
    H = nmf.components_
    print 'reconstruction error:', nmf.reconstruction_err_

    # hand_labels = hand_label_topics(H, vocabulary)
    #
    # for i in rand_articles:
    #     analyze_article(i, contents, web_urls, W, hand_labels)

if __name__ == '__main__':
    main()
