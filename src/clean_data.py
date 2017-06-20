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

pd.options.display.max_colwidth = 700

client = MongoClient('localhost:27017')

def strip_non_ascii(string):
    ''' 
    Removes non-ascii characters from string
    INPUT: string
    OUTPUT: string with only ascii characters
    '''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)

def remove_unicode(row):
    '''
    Removes unicode characters from string
    INPUT: string
    OUTPUT: string with no unicode characters 
    '''
    return [r.decode('unicode_escape').encode('ascii', 'ignore') for r in row]

def read_ajc_mongodb_data():
    '''
    Read in AJC articles from MongoDB
    Does some cleaning specific to the AJC articles
    OUTPUT: df: DataFrame 
    '''
    db = client.newsarticles
    df = pd.DataFrame(list(db.articles.find({'source': 'ajc'})))
    df['title'] = df['title'].apply(strip_non_ascii)
    df['title'] = df['title'].astype(str)
    df['article'] = df['content'].apply(strip_non_ascii)
    df['article'] = df['article'].astype(str).str.strip()
    df['article'] = df['article'].str.replace(r"BY[^\\]*","")
    return df

def read_den_mongodb_data():
    '''
    Read in Denver Post articles from MongoDB
    Does some cleaning specific to the Denver Post articles
    OUTPUT: df: DataFrame 
    '''
    db = client.denpost
    df = pd.DataFrame(list(db.articles.find()))
    df['title'] = df['title'].apply(lambda x: ', '.join(x))
    df['title'] = df['title'].apply(strip_non_ascii)
    df['article'] = df['article'].astype('str').apply(strip_non_ascii)
    return df

def read_latimes_mongodb_data():
    '''
    Read in LATimes articles from MongoDB
    Does some cleaning specific to the LATimes articles
    OUTPUT: df: DataFrame 
    '''
    db = client.latimes_good
    df = pd.DataFrame(list(db.articles.find()))
    df['title'] = df['title'].astype(str)
    df['article'] = df['article'].apply(strip_non_ascii)
    df['article'] = df['article'].astype(str).str.strip()
    return df

def clean_text(contents):
    '''
    Cleans strings in articles
    INPUT: 
        df: str (default = None) article in string format
    OUTPUT: df: cleaned article in string format
    '''
    # remove 'by author'
    contents = contents.str.replace(r"By[^,]*","")
    contents = contents.str.replace('U.S.', 'United States')
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
    pt = set(punctuation)
    contents = contents.apply(lambda x: ''.join([" " if  i in pt else i for i in x]))
    return contents


def fix_lemmatized_words():
    '''
    OUTPUT: dict - A dictionary mapping the lemmatized word to what the word should actually be.
    The lemmatizer generally works well but shortens some words incorrectly (e.g. 'texas' -> 'texa', 'paris' -> 'pari', 'fetus' -> 'fetu').  This dictionary will correct some of the more blatent errors after lemmatizing
    '''
    correct_lemma = {
    'pari': 'paris',
    'infectiou': 'infectious',
    'dangerou': 'dangerous',
    'texa': 'texas',
    'religiou': 'religious',
    'chri': 'chris',
    'congres': 'congress',
    'hatre': 'hatred',
    'isi': 'isis',
    'massachusett': 'massachusetts',
    'arkansa': 'arkansas',
    'ridiculou': 'ridiculous',
    'abba': 'abbas',
    'campu': 'campus',
    'fundrais': 'fundraise',
    'crisi': 'crisis',
    'cannabi': 'cannabis',
    'sander': 'sanders',
    'davi': 'davis',
    'franci': 'francis',
    'orlean': 'orleans',
    'vega': 'vegas',
    'kansa': 'kansas'
    }
    return correct_lemma

def lemmatize_article(article):
    '''
    Lemmatize the given article 
    INPUT: article (str) - raw text from the article (where text has been lowered and punctuation removed already)
    OUTPUT: lemmatized_article - article text with all stopwords removed and the remaining text lemmatized
    '''
    stop_lemma_words = ['was', 'has', 'u', 's']
    # Load Dictionary to fix commonly mislemmatized words
    correct_lemma = fix_lemmatized_words()
    # Lemmatize article by running each word through the pattern.en lemmatizer and only 
    # including it in the resulting text if the word doesn't appear in the set of stopwords
    #article = ' '.join([en.lemma(w) for w in article.split() if w not in stop_lemma_words])
    article = ' '.join([w for w in article.split() if w not in stop_lemma_words])
    # Return the article text after fixing common mislemmatized words
    return ' '.join([correct_lemma[w] if w in correct_lemma else w for w in article.split()])


if __name__ == '__main__':
    '''
    Read the data from MongoDB.
    Clean the data
    Creates dataframe with cleaned articles
    USAGE:  clean_data newspaper
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
    print("Number of articles")
    print(len(df))
    #contents = df['article'].astype(str).str.encode('utf-8')

    contents = df['article']

    #Examine articles pre-cleaning
    print("Precleaning")
    print(df['article'].astype(str).str.encode('utf-8'))

    clean_contents = clean_text(contents)
    #lemmatize the cleaned articles
    doc_clean = [lemmatize_article(doc) for doc in clean_contents]
    df['clean_article'] = doc_clean

    #Examine articles post-cleaning
    print
    print
    print("Post cleaning")
    print(df['clean_article'])


    # Save the pickled dataframe later access 
    path = '/Users/jenniferkey/galvanize/nlp-gender-news/data/{}/clean_df.pkl'.format(news_paper)
    df.to_pickle(path)
