import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from nltk.corpus import stopwords
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.lancaster import LancasterStemmer
import cPickle as pickle

# Creating a class for topic modeling.  Will pick up again after presentation


Class TopicModel(object):

    def __init__(self, type, no_topics, max_features=1000, max_iter=150, max_df=.95,
    min_df=1, random_state=1, alpha=.01, l1_ratio=.5, init='nndsvd',
    learning_offset=50, stop_words=stop_set):
        self.type = type
        self.no_topics = no_topics
        self.max_features = max_features
        if self.type = 'NMF':
            self.max_iter = 150
        else:
            self.max_iter = 5
        self.max_df = max_df
        self.min_df = min_df
        self.random_state = random_state
        self.alpha = alpha
        self.l1_ratio = l1_ratio
        self.init = init
        self.learning_offset = learning_offset

    def fit(self, df, l_doc):
        '''
        Build topics using specified algorithm 'NMF' or 'LDA'.
        Input pandas dataframe with cleaned and lemmatized or stemmed column.
        '''
        self.df = df
        self.l_doc = l_doc
        if self.type = 'NMF':
            # For NMF use tfidf vectorizer

    def tfidf_vect(self):
        '''
        Creates teh tfidf vectorizer using lemmatized or stemmed column from dataframe
        '''
        #Instaniate a tfidf vectorizer
        self.tfidf_vectorizer = TfidfVectorizer( max_df=self.max_df, min_df=self.min_df, max_features=self.max_features, stop_words=self.stop_words)

        # Fit tfidf
        self.tfidf = tfidf_vectorizer.fit_transform(self.l_doc)
        tfidf_feature_names = tfidf_vectorizer.get_feature_names()
