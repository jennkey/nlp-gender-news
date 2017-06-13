import numpy as np
import pandas as pd
import re
import pdb

from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
#from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.lancaster import LancasterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF
from sklearn.decomposition import LatentDirichletAllocation


import collections

import matplotlib.pyplot as plt
from wordcloud import WordCloud


# Closure over the tokenizer et al.
def tokenize(text):
    tokens = tokenizer.tokenize(text)
    stems = [stem(token) for token in tokens if token not in stop_set]
    return stems

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
        top_five = np.argsort(row)[::-1][:30]
        print ('topic', i)
        print ('-->', ' '.join(vocabulary[top_five]))
        label = raw_input('please label this topic: ')
        hand_labels.append(label)
        print()
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
    print( web_urls[article_index])
    print (contents[article_index])
    probs = softmax(W[article_index], temperature=0.01)
    for prob, label in zip(probs, hand_labels):
        print ( '--> {:.2f}% {}'.format(prob * 100, label))
    print


def label_articles():
    for topic in topics:
        topic_labels.append(hand_labels[topic])
    #Need to update the mongo db with the topic label_articles
    # may need to somehow have kept the id field here is some sample code
    db.Doc.update({"_id": b["_id"]}, {"$set": {"geolocCountry": myGeolocCountry}})

def display_topics(model, feature_names, no_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print ("Topic %d:" % (topic_idx))
        print( " ".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]]))


def display_topics_full(H, W, feature_names, documents, no_top_words, no_top_documents):
    for topic_idx, topic in enumerate(H):
        print("Topic %d:" % (topic_idx))
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

    df = pd.read_pickle('/Users/jenniferkey/galvanize/nlp-gender-news/data/clean_df.pkl')
    contents = df['clean_article']

    #NMF - use td-idf
    # Build our text-to-vector vectorizer, then vectorize our corpus.
    #vectorizer, vocabulary = build_text_vectorizer(contents, use_tfidf=True,
    #                             use_stemmer=True,
    #                             max_features=500)
    #X = vectorizer(contents)
    no_features = 1000
    tokenizer = RegexpTokenizer(r"[\w']+")

    stop_set = set(stopwords.words('english'))
    stop_set.update(['said', 'say', 'thing', 'know', 'like'])

    #stem = PorterStemmer().stem
    lancaster_stemmer = LancasterStemmer()

    # NMF is able to use tf-idf
    tfidf_vectorizer = TfidfVectorizer(tokenizer=tokenize, max_df=0.95, min_df=1, max_features=no_features, stop_words=stop_set)
    tfidf = tfidf_vectorizer.fit_transform(contents)
    tfidf_feature_names = tfidf_vectorizer.get_feature_names()

    #LDA uses counts
    tf_vectorizer = CountVectorizer(tokenizer=tokenize, max_df=0.95, min_df=1, max_features=no_features, stop_words=stop_set)
    tf = tf_vectorizer.fit_transform(contents)
    tf_feature_names = tf_vectorizer.get_feature_names()

    #set topic number
    no_topics = 15
    no_top_words = 15
    no_top_documents = 5

    # Run NMF
    nmf = NMF(n_components=no_topics, max_iter=150, random_state=1, alpha=.01, l1_ratio=.5, init='nndsvd').fit(tfidf)
    W_nmf = nmf.fit_transform(tfidf)
    H_nmf = nmf.components_
    print ('reconstruction error:', nmf.reconstruction_err_)
    topics_nmf = np.argmax(W_nmf, axis=1)
    num_articles_nmf = collections.Counter(topics_nmf)
    print("Number of articles in each topic NMF")
    print(num_articles_nmf)
    #display_topics(nmf, tfidf_feature_names, no_top_words)
    display_topics_full(H_nmf, W_nmf, tfidf_feature_names, contents, no_top_words, no_top_documents)
    #for each topic create a word cloud
    path_plot = '/Users/jenniferkey/galvanize/nlp-gender-news/plots/'
    for topic_indx in range(no_topics):
        file_name = path_plot + 'nmf_topic_{}_cloud.png'.format(topic_indx)
        topic_word_cloud(topic_indx)
        plt.savefig(file_name, dpi=250)
        plt.close()


    # Run LDA
    # lda = LatentDirichletAllocation(n_topics=no_topics, max_iter=5, learning_method='online', learning_offset=50.,random_state=0).fit(tf)
    # W_lda = lda.transform(tf)
    # H_lda = lda.components_
    # topics_lda = np.argmax(W_lda, axis=1)
    # num_articles_lda = collections.Counter(topics_lda)
    # print("Number of articles in each topic LDA")
    # print(num_articles_lda)
    # #display_topics(lda, tf_feature_names, no_top_words)
    # display_topics_full(H_lda, W_lda, tf_feature_names, contents, no_top_words, no_top_documents)

    #word_cloud()

    # Display topics

    #print ("NFM")


    #choose topic for each document
    topics = np.argmax(W_nmf, axis=1)
    df['topic'] = topics

    # Save the pickled dataframe for easy access later
    df.to_pickle('/Users/jenniferkey/galvanize/nlp-gender-news/data/topic_unlabeled_data.pkl')


    #print ("LDA")
    #display_topics(lda, tf_feature_names, no_top_words)
    #display_topics_full(H_lda, W_lda, tf_feature_names, contents, no_top_words, no_top_documents)




    # match up titles to topics

    #hand_labels = hand_label_topics(H, vocabulary)
    #
    # for i in rand_articles:
    #     analyze_article(i, contents, web_urls, W, hand_labels)

# if __name__ == '__main__':
#     main()
