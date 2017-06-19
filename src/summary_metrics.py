import pandas as pd
import plotly.plotly as py
import plotly
import plotly.graph_objs as go
from plotly import tools
import numpy as np
from source_by_topic_bubbles import bubble_by_source_by_topic

# creates summary metrics for all sources

def read_pickle_df(news_paper):
    '''
    Reads in pickled dataframe for each newspaper
    '''
    datapath = '/Users/jenniferkey/galvanize/nlp-gender-news/data/{}/'.format(news_paper)
    pickle_to_read = datapath + 'df_gendered_articles.pkl'
    df = pd.read_pickle(pickle_to_read)
    return df

def summary_metrics(df, source):
    '''
    Creates summary metrics for each newspaper
    '''

    sources.append(source)
    #overall ratio of male sentences to female sentences
    male_to_female_ratio = (df['male_sentences'].sum() + df['both_sentences'].sum()) / (df['female_sentences'].sum() + df['both_sentences'].sum())
    ratio_male_to_female_sentences_list.append(male_to_female_ratio)

    print(source)
    male_articles = len(df[(df['female_sentences'] < df['male_sentences'])])
    print('Male articles', male_articles)
    female_articles = len(df[(df['female_sentences'] > df['male_sentences'])])
    print('Female articles', female_articles)
    ratio_male_to_female_articles_list.append(male_articles/female_articles)

def aggregate_by_topic(df_unagg):
    df_agg = df_unagg[['topic_label', 'male_sentences', 'both_sentences', 'female_sentences']].groupby(['topic_label']).sum()
    df_agg['topic_count'] = df_unagg[['topic_label']].groupby(['topic_label']).size()
    print(df_agg)
    return df_agg


def fix_source(df):
    new_source = []
    for source in df['source']:
        if source in ('ajc', 'latimes'):
            new_source.append(source)
        else:
            new_source.append(''.join(str(e) for e in source))
    df['source'] = new_source

def count_source(df):
    source_dict = {}
    for source in df['source']:
        source = ''.join(str(e) for e in source)
        if source in source_dict:
            source_dict[source] += 1
        else:
            source_dict[source] = 1
    print(source_dict)


if __name__ == '__main__':
    news_papers = ['ajc', 'denver_post', 'latimes']
    pretty_names = ["Atlantic Journal Constitution", "The Denver Post", "Los Angeles Times"]
    # read in pickled dataframe with topics and labels
    df = read_pickle_df('all')

    # Print out counts of each source
    fix_source(df)
    print(pd.value_counts(df['source']))
    ratio_male_to_female_articles_list = []
    ratio_male_to_female_sentences_list = []

    count_source(df)

    # create a dataframe for each source -- change this later but for now need to
    # do it this way since running out of time and code already expecting this
    ajc = df[(df['source'] == 'ajc')]
    latimes = df[(df['source'] == 'latimes')]
    denver_post = df[(df['source'] == 'Denver Post')]


    sources = []
    ratio_male_to_female_articles_list = []
    ratio_male_to_female_sentences_list = []
    summary_metrics(df, 'All')
    summary_metrics(ajc, 'AJC')
    summary_metrics(latimes, 'LA Times')
    summary_metrics(denver_post, 'Denver Post')
    print(sources)
    print(ratio_male_to_female_articles_list)
    print(ratio_male_to_female_sentences_list)

    # create male_percent and female_percent by topic by source
    df_agg_all = aggregate_by_topic(df)
    df_agg_ajc = aggregate_by_topic(ajc)
    df_agg_latimes = aggregate_by_topic(latimes)
    df_agg_denver_post = aggregate_by_topic(denver_post)

    # append all the aggregated data together just to make it easier to work with
    df_allsource = df_agg_ajc.append(df_agg_latimes, ignore_index=True)
    df_allsource = df_allsource.append(df_agg_denver_post, ignore_index=True)

    # create plots for each topic label showing all three sources
    topic_labels = list(df_all_all['topic_label'])
    for topic in topic_labels:
        bubble_by_source_by_topic(topic)


    #bar_chart()
