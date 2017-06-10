import numpy as np
import pandas as pd
import re
import pdb
from pymongo import MongoClient

client = MongoClient('localhost:27017')


# function to read records from mongo db
def read_mongodb_data(mongodb_toread):
    db = client.denpost
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

if __name__ == '__main__':
    '''
    Read the data from MongoDB.
    Use NMF to find latent topics.
    '''

    #Read data from MongoDB
    df = read_mongodb_data('denpost')

    df['title'] = df['title'].apply(lambda x: ', '.join(x))
    print("Number of article pre-dedupe:", len(df))
    df = df.drop_duplicates('title')
    print("Number of articles post-dedupe:", len(df))

    df['article'] = df['article'].apply(lambda x: ', '.join(x))
    contents = df['article']

    df['clean_article'] = clean_text(contents)

    # Save the pickled dataframe for easy access later
    df.to_pickle('/Users/jenniferkey/galvanize/nlp-gender-news/data/clean_df.pkl')
