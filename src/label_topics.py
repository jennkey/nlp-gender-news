import pandas as pd
import numpy as np


if __name__ == '__main__':


    #read in pickled data frame with raw topics
    df = pd.read_pickle('/Users/jenniferkey/galvanize/nlp-gender-news/data/clean_df.pkl')

    #choose topic for each document
    topics = np.argmax(W_nmf, axis=1)
    df['topic'] = topics

    # read from stdin or file on command line.
    topics_label = []
    for line in fileinput.input():
        topics_label.append(line.replace('\n',''))


    df['topic_label'] = topic_label

    df.to_pickle('/Users/jenniferkey/galvanize/nlp-gender-news/data/topic_data_with_label.pkl')
