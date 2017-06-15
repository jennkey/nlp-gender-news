import pandas as pd
import numpy as np
import fileinput
import sys


if __name__ == '__main__':

    news_paper = sys.argv[1]

    #read in pickled data frame with raw topics
    datapath = '/Users/jenniferkey/galvanize/nlp-gender-news/data/{}/'.format(news_paper)
    topic_unlabeled_file = datapath + 'topic_unlabeled.pkl'
    df = pd.read_pickle(topic_unlabeled_file)

    # read from stdin or file on command line.
    labels_file = datapath + 'topics_labels.csv'
    topic_label_list = []
    for line in fileinput.input(labels_file):
        topic_label_list.append(line.replace('\n',''))

    # assign topic label to each article
    topic_label = []
    for topic in df['topic']:
        topic_label.append(topic_label_list[topic])

    df['topic_label'] = topic_label

    topic_labeled_file = datapath + 'topic_labeled.pkl'
    df.to_pickle(topic_labeled_file)
