import numpy as np
import pandas as pd
import re
import pdb
import sys
from pymongo import MongoClient
from string import punctuation
from string import printable
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer

#from pandas import compat

#compat.PY3 = True

client = MongoClient('localhost:27017')

def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)

# function to read records from mongo db
def read_ajc_mongodb_data():
    db = client.newsarticles
    df = pd.DataFrame(list(db.articles.find({'source': 'ajc'})))
    #df2 = pd.DataFrame(list(db_2.articles.find()))
    #df = pd.concat([df1, df2])
    df['title'] = df['title'].apply(strip_non_ascii)
    df['title'] = df['title'].astype(str)
    df['article'] = df['content'].apply(strip_non_ascii)
    df['article'] = df['article'].astype(str).str.strip()
    df['article'] = df['article'].str.replace(r"BY[^\\]*","")
    return df

def read_den_mongodb_data():
    db1 = client.denpost
    db2 = client.news
    df1 = pd.DataFrame(list(db1.articles.find()))
    df2 = pd.DataFrame(list(db2.articles.find()))
    df = pd.concat([df1, df2])
    df['title'] = df['title'].apply(lambda x: ', '.join(x))
    df['article'] = df['article'].apply(lambda x: ', '.join(x))
    df['title'] = df['title'].apply(strip_non_ascii)
    df['article'] = df['article'].apply(strip_non_ascii)
    #df['article'] = df['article'].apply(strip_non_ascii)
    return df

def read_latimes_mongodb_data():
    db = client.latimes_good
    df = pd.DataFrame(list(db.articles.find()))
    #df2 = pd.DataFrame(list(db_2.articles.find()))
    #df = pd.concat([df1, df2])
    df['title'] = df['title'].astype(str)
    df['article'] = df['article'].apply(strip_non_ascii)
    df['article'] = df['article'].astype(str).str.strip()
    return df

def clean_text(contents):
    # remove 'by author'
    contents = contents.str.replace(r"By[^,]*","")
    #lower case all text
    contents = contents.str.lower()
    # change contractions to their long form
    contents = contents.str.replace("what's", "what is ")
    contents = contents.str.replace("\'ve", " have ")
    contents = contents.str.replace("can't", "cannot ")
    contents = contents.str.replace("n't", " not ")
    contents = contents.str.replace("I'm", "I am ")
    contents = contents.str.replace(r"\'re", " are ")
    contents = contents.str.replace(r"\'d", " would ")
    contents = contents.str.replace(r"\'ll", " will ")
    contents = contents.str.replace('\n', '')
    contents = contents.str.replace(r'\d+','')
    contents = contents.str.replace("view caption hide caption", "")
    st = set(printable)
    contents = contents.apply(lambda x: ''.join([" " if  i not in st else i for i in x]))
    #remove punctuation
    #contents=[w.strip(punctuation) for w in contents if len(w.strip(punctuation))>0]
    pt = set(punctuation)
    contents = contents.apply(lambda x: ''.join([" " if  i in pt else i for i in x]))

    return contents

def lemmatize_article(text):
    '''
    INPUT: text to be lemmatized
    OUTPUT: lemmatized text
    '''
    #remove some words that get lemmatized in a strange way
    stop_lemma_words = ['was', 'has']
    lemma = WordNetLemmatizer()
    contents = " ".join(lemma.lemmatize(word) for word in text.split() if not word in stop_lemma_words)
    #print contents
    #contents = [', '.join(list) for list in contents]
    #print type(contents)
    #contents = [list.replace(',','') for list in contents]
    return contents


if __name__ == '__main__':
    '''
    Read the data from MongoDB.
    Use NMF to find latent topics.
    '''
    #read in newspaper to clean from argument
    news_paper = sys.argv[1]

    #Read data from MongoDB
    if news_paper == 'denver_post':
        df = read_den_mongodb_data()
    elif news_paper == 'latimes':
        df = read_latimes_mongodb_data()
    elif news_paper == 'ajc':
        df = read_ajc_mongodb_data()

    #df['title'] = df['title'].apply(lambda x: ', '.join(x))
    print("Number of article pre-dedupe:", len(df))
    df['title'] = df['title'].astype('str').str.encode('utf-8')
    df = df.drop_duplicates('title')
    print("Number of articles post-dedupe:", len(df))

    #Still have duplicate articles so need to dedupe based on the first few sentences of the article itself.
    df['first_few'] = df['article'].str[:100]
    df = df.drop_duplicates('first_few')
    print("Number of article post-dedupe on article", len(df))

    #df['article'] = df['article'].apply(lambda x: ', '.join(x))
    df['article'].str.strip()
    print(len(df))
    #contents = df['article'].astype(str).str.encode('utf-8')

    contents = df['article']

    print("Precleaning")
    print(df['article'].astype(str).str.encode('utf-8'))


    clean_contents = clean_text(contents)
    #lemmatize the cleaned articles
    doc_clean = [lemmatize_article(doc) for doc in clean_contents]
    df['clean_article'] = doc_clean

    print
    print
    print("Post cleaning")
    print(df['clean_article'])


    # Save the pickled dataframe for easy access later
    path = '/Users/jenniferkey/galvanize/nlp-gender-news/data/{}/clean_df.pkl'.format(news_paper)
    df.to_pickle(path)
