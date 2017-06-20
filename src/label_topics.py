import pandas as pd
import numpy as np
import fileinput
import sys
import csv

def create_groups(row):
    group1 = ['Arts/Cultural', 'Books', 'Entertainment', 'Food', 'Gardening',
                  'Lifestyle', 'Music']
    group2 = ['U.S. Politics', 'Local Politics/Government', 'International','Russia Investigation']
    if row['topic_label'] in group1:
        return 'Lifestyle'
    if row['topic_label'] in group2:
        return 'Politics'
    else:
        return row['topic_label']


if __name__ == '__main__':

    news_paper = sys.argv[1]

    #read in pickled data frame with raw topics
    datapath = '/Users/jenniferkey/galvanize/nlp-gender-news/data/{}/'.format(news_paper)
    topic_unlabeled_file = datapath + 'topic_unlabeled_{}.pkl'.format(news_paper)
    df = pd.read_pickle(topic_unlabeled_file)

    # read from stdin or file on command line.
    labels_file = datapath + 'topic_labels.csv'
    topic_label_list = []
    with open(labels_file, 'r') as csvfile:
        labelreader = csv.reader(csvfile)
        for row in labelreader:
            print(row)
            topic = ', '.join(row)
            topic_label_list.append(topic)


    # assign topic label to each article
    topic_label = []
    for topic in df['topic']:
        #topic_label.append(topic_label_list[topic])
        topic_label.append(topic_label_list[topic])

    df['topic_label'] = topic_label

    # Create group field
    df['group'] = df.apply(lambda row: create_groups(row), axis=1)

    topic_labeled_file = datapath + 'topic_labeled.pkl'
    df.to_pickle(topic_labeled_file)
