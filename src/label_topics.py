import pandas as pd
import numpy as np
import fileinput
import sys
import csv

if __name__ == '__main__':

    topic_label_list = []
    for i in range(50):
        topic_label_list.append('topic{}'.format(i))
    print(topic_label_list)

    news_paper = sys.argv[1]

    #read in pickled data frame with raw topics
    datapath = '/Users/jenniferkey/galvanize/nlp-gender-news/data/{}/'.format(news_paper)
    topic_unlabeled_file = datapath + 'topic_unlabeled.pkl'
    df = pd.read_pickle(topic_unlabeled_file)

    # read from stdin or file on command line.
    labels_file = datapath + 'topics_labels.csv'
    # topic_label_list = []
    # with open(labels_file, 'rb') as csvfile:
    #     labelreader = csv.reader(csvfile)
    #     for row in labelreader:
    #         print row
    #         topic = ', '.join(row)
    #         topic_label_list.append(topic)


    # assign topic label to each article
    topic_label = []
    for topic in df['topic']:
        topic_label.append(topic_label_list[topic])

    df['topic_label'] = topic_label

    topic_labeled_file = datapath + 'topic_labeled.pkl'
    df.to_pickle(topic_labeled_file)
