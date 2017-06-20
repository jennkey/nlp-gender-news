import numpy as np
import pandas as pd
import re
import pdb

from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.lancaster import LancasterStemmer
from nltk.s
from item.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF
from sklearn.decomposition import LatentDirichletAllocation
import sys
import os

import collections

import matplotlib.pyplot as plt
from wordcloud import WordCloud

def make_dir(directory):
    '''
    If directory does not exist it creates one
    INPUT:
        directory: (str) Directory to be created if necessary (include path)
    OUTPUT: NONE
    '''
    if not os.path.exists(directory):
        os.makedirs(directory)

def read_df(news_paper):
    '''
    Creates a dataframe for topic modeling based on user input
    INPUT: news_paper (str) indicates which data sources to use
           for topic modeling.
           all = Use all newspapers
           nest = Use a subset of articles based on previously created topics
           female = Use only articles identified as majority female to create topics
           male = Use only articles identified as majority male to create topics
    OUTPUT: 
             df,
             datapath, 
             plotpath, 
             final_pickle

    '''
    if news_paper == 'all':
        datapath = '/Users/jenniferkey/galvanize/nlp-gender-news/data/all/'
        file1 = '/Users/jenniferkey/galvanize/nlp-gender-news/data/denver_post/clean_df.pkl'
        file2 = '/Users/jenniferkey/galvanize/nlp-gender-news/data/latimes/clean_df.pkl'
        file3 = '/Users/jenniferkey/galvanize/nlp-gender-news/data/ajc/clean_df.pkl'
        plotpath = '/Users/jenniferkey/galvanize/nlp-gender-news/plots/all/'
        df_denverpost = pd.read_pickle(file1)
        df_latimes = pd.read_pickle(file2)
        df_ajc = pd.read_pickle(file3)
        df = df_denverpost.append(df_latimes, ignore_index=True)
        df = df.append(df_ajc, ignore_index=True)

    elif 'nest' in news_paper:
        datapath = '/Users/jenniferkey/galvanize/nlp-gender-news/data/all/{}/'.format(news_paper)
        plotpath = '/Users/jenniferkey/galvanize/nlp-gender-news/plots/all/{}/'.format(news_paper)
        make_dir(datapath)
        make_dir(plotpath)

        if len(news_paper) == 4:
            topic = int(news_paper[4])
        else:
            topic = int(news_paper[4:6])

        clean_file = '/Users/jenniferkey/galvanize/nlp-gender-news/data/all/topic_unlabeled.pkl'
        df = pd.read_pickle(clean_file)
        df = df[(df['topic'] == topic)]

    elif 'female' in news_paper:
        datapath = '/Users/jenniferkey/galvanize/nlp-gender-news/data/all/{}/'.format(news_paper)
        plotpath = '/Users/jenniferkey/galvanize/nlp-gender-news/plots/all/{}/'.format(news_paper)
        make_dir(datapath)
        make_dir(plotpath)
        gendered_articles = '/Users/jenniferkey/galvanize/nlp-gender-news/data/all/df_gendered_articles.pkl'
        df = pd.read_pickle(gendered_articles)
        df = df[(df['female_sentences'] > df['male_sentences'])]

    elif 'male' in news_paper:
        datapath = '/Users/jenniferkey/galvanize/nlp-gender-news/data/all/{}/'.format(news_paper)
        plotpath = '/Users/jenniferkey/galvanize/nlp-gender-news/plots/all/{}/'.format(news_paper)
        make_dir(datapath)
        make_dir(plotpath)
        gendered_articles = '/Users/jenniferkey/galvanize/nlp-gender-news/data/all/df_gendered_articles.pkl'
        df = pd.read_pickle(gendered_articles)
        df = df[(df['female_sentences'] < df['male_sentences'])]

    final_pickle =  datapath + 'topic_unlabeled_{}.pkl'.format(news_paper)
    return df, datapath, plotpath, final_pickle



def tokenize(text):
    '''
    Tokenizes given text
    INPUT: text (str)
    OUTPUT: stems (list of stemmed words)
    '''
    tokens = tokenizer.tokenize(text)
    stems = [stem(token) for token in tokens if token not in stop_set]
    return stems

def grid_number_topics(start, stop, increment):
    '''
    Iteratively builds NMF for different numbers of topics and produces the reconstruction error
    plot
    INPUT: start (int) - minimum number of topics to build
           stop (int) -  maximum number of topics to build 
           inc (int) - increments to increase number of topics by
    OUTPUT:  plot of reconstruction errors
    '''
    recon_error_list = []
    number_topics = []
    for i in range(start, stop, increment):
        nmf = NMF(n_components=i, max_iter=150, random_state=1, alpha=.01, l1_ratio=.5, init='nndsvd').fit(tfidf)
        W_nmf = nmf.fit_transform(tfidf)
        H_nmf = nmf.components_
        recon_error_list.append(nmf.reconstruction_err_)
        number_topics.append(i)
        print ('topic_number, reconstruction error:', i, nmf.reconstruction_err_)

    recon_error_plot(number_topics=number_topics, recon_error_list=recon_error_list)

def recon_error_plot(number_topics, recon_error_list, figsize=(14,8)):
    # Create the matplotlib figure and axis if they weren't passed in
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111)
    ax.plot(number_topics, recon_error_list)
    ax.set(title='Reconstruction Error',
           ylabel='Reconstruction Error',
           xlabel='Number of Topics')
    plt_file = plotpath + 'reconstruction_error.png'
    plt.savefig(plt_file, dpi=250)
    plt.close()


def perform_NMF(no_topics=15, no_top_words=15, no_top_documents=5):
    # Run NMF
    nmf = NMF(n_components=no_topics, max_iter=150, random_state=1, alpha=.01, l1_ratio=.5, init='nndsvd').fit(tfidf)
    W_nmf = nmf.fit_transform(tfidf)
    H_nmf = nmf.components_
    print ('reconstruction error:', nmf.reconstruction_err_)
    topics_nmf = np.argmax(W_nmf, axis=1)
    num_articles_nmf = collections.Counter(topics_nmf)
    display_topics_full(H_nmf, W_nmf, tfidf_feature_names, contents, no_top_words, no_top_documents, num_articles_nmf)
    return W_nmf, H_nmf, topics_nmf

def peform_LDA():
    #Run LDA
    lda = LatentDirichletAllocation(n_topics=no_topics, max_iter=5, learning_method='online', learning_offset=50.,random_state=0).fit(tf)
    W_lda = lda.transform(tf)
    H_lda = lda.components_
    topics_lda = np.argmax(W_lda, axis=1)
    num_articles_lda = collections.Counter(topics_lda)
    display_topics_full(H_lda, W_lda, tf_feature_names, contents, no_top_words, no_top_documents)
    return W_lda, H_lda, topics_lda


def display_topics(model, feature_names, no_top_words):
    num_articles = 'num_articles_{}'.format(model)
    for topic_idx, topic in enumerate(model.components_):
        print ("Topic %d:" % (topic_idx))
        print ("Number of articles %d:" % (num_articles[topic_idx]))
        print( " ".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]]))


def display_topics_full(H, W, feature_names, documents, no_top_words, no_top_documents, num_articles):
    for topic_idx, topic in enumerate(H):
        print("Topic %d:" % (topic_idx))
        print ("Number of articles %d:" % (num_articles[topic_idx]))
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-no_top_words - 1:-1]]))
        top_doc_indices = np.argsort( W[:,topic_idx] )[::-1][0:no_top_documents]
        for doc_index in top_doc_indices:
            print(documents.iloc[doc_index][0:40])


def topic_word_freq(topic_indx):
    freq_sum = np.sum(H_nmf[topic_indx])
    frequencies = [val /freq_sum for val in H_nmf[topic_indx]]
    return dict(zip(tfidf_feature_names, frequencies))

def topic_word_cloud(topic_indx, max_words=300, figsize=(14, 8), width=2400, height=1300, ax=None):
    ''' Create word cloud for a given topic
    INPUT:
        topic_idx: int
        max_words: int
            Max number of words to encorporate into the word cloud
        figsize: tuple (int, int)
            Size of the figure if an axis isn't passed
        width: int
        height: int
        ax: None or matplotlib axis object
    '''
    wc = WordCloud(background_color='white', max_words=max_words, width=width, height=height)
    word_freq_dict = topic_word_freq(topic_indx)

    # Fit the WordCloud object to the specific topics word frequencies
    wc.fit_words(word_freq_dict)

    # Create the matplotlib figure and axis if they weren't passed in
    if not ax:
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111)
    ax.imshow(wc)
    ax.axis('off')



if __name__ == '__main__':
    '''
    Using cleaned pickled pandas dataframe
    Use NMF and LDA to find latent topics.
    '''

    #read in newspaper to clean from argument
    news_paper = sys.argv[1]

    #read in pickle
    df, datapath, plotpath, final_pickle = read_df(news_paper)
    contents = df['clean_article']
    print (len(contents))

    #NMF - use td-idf
    # Build our text-to-vector vectorizer, then vectorize our corpus.
    #vectorizer, vocabulary = build_text_vectorizer(contents, use_tfidf=True,
    #                             use_stemmer=True,
    #                             max_features=500)
    #X = vectorizer(contents)
    no_features = 1000
    tokenizer = RegexpTokenizer(r"[\w']+")

    stop_set = set(stopwords.words('english'))
    stop_set.update(['said', 'say', 'thing', 'know', 'like', 'thi', 'was', 'has', 'u', 's'
                     'www', 'ajc'])

    #stem = PorterStemmer().stem
    #stem = LancasterStemmer().stem
    #stem = SnowballStemmer('english').stem
    stem = WordNetLemmatizer().lemmatize

    # NMF is able to use tf-idf
    tfidf_vectorizer = TfidfVectorizer(tokenizer=tokenize, max_df=0.95, min_df=1, max_features=no_features, stop_words=stop_set)
    tfidf = tfidf_vectorizer.fit_transform(contents)
    tfidf_feature_names = tfidf_vectorizer.get_feature_names()

    #LDA uses counts
    tf_vectorizer = CountVectorizer(tokenizer=tokenize, max_df=0.95, min_df=1, max_features=no_features, stop_words=stop_set)
    tf = tf_vectorizer.fit_transform(contents)
    tf_feature_names = tf_vectorizer.get_feature_names()

    # Grid search for right number of topics
    #grid_number_topics(1, 60, 1)

    #set topic number
    W_nmf, H_nmf, topics = perform_NMF(no_topics=60, no_top_words=15, no_top_documents=5)

    #Create word clouds
    #for each topic create a word cloud
    for topic_indx in range(len(H_nmf)):
        file_name = plotpath + 'nmf_topic_{}_cloud.png'.format(topic_indx)
        topic_word_cloud(topic_indx, 100)
        plt.savefig(file_name, dpi=250)
        plt.close()

    df['topic'] = topics

    # Save the pickled dataframe for easy access later

    df.to_pickle(final_pickle)


    #print ("LDA")
    #display_topics(lda, tf_feature_names, no_top_words)
    #display_topics_full(H_lda, W_lda, tf_feature_names, contents, no_top_words, no_top_documents)


    #hand_labels = hand_label_topics(H, vocabulary)
    #
    # for i in rand_articles:
    #     analyze_article(i, contents, web_urls, W, hand_labels)

# if __name__ == '__main__':
#     main()
