import pandas as pd
import plotly.plotly as py
import plotly
import plotly.graph_objs as go
from plotly import tools
import numpy as np
from source_by_topic_bubbles_simple import bubble_by_source_by_topic
from bubble import all_topics_bubble
from bar_ratio_chart import bar_ratio_chart
from bar_ratio_chart import bubble_ratio_chart
from bar_ratio_chart import bubble_ratio_chart_by_source


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

def aggregate_by_topic(df_unagg, source, level='topic_label'):
    df_agg = df_unagg[[level, 'male_sentences', 'both_sentences', 'female_sentences']].groupby([level]).sum()
    df_agg['topic_count'] = df_unagg[[level]].groupby([level]).size()
    count_all_sentences = df_agg['male_sentences'] + df_agg['female_sentences'] + df_agg['both_sentences']
    df_agg['male_percent'] = (df_agg['male_sentences'] + df_agg['both_sentences'])/count_all_sentences
    df_agg['female_percent'] = (df_agg['female_sentences'] + df_agg['both_sentences'])/ count_all_sentences
    df_agg['ratio'] = df_agg['male_percent']/df_agg['female_percent']
    df_agg['source'] = source
    df_agg.reset_index(level=0, inplace=True)
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


def create_dummy_groups(row):
    if row['group'] == 'Sports':
        return 'A'
    elif row['group'] == 'Politics':
        return 'B'
    elif row['group'] == 'Business':
        return 'C'
    elif row['group'] == 'Real Estate':
        return 'D'
    elif row['group'] == 'Crime':
        return 'E'
    elif row['group'] == 'Lifestyle':
        return 'F'
    elif row['group'] == 'Education':
        return 'G'




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
    df_agg_all = aggregate_by_topic(df, 'all')
    df_agg_all_group = aggregate_by_topic(df, 'all', 'group')
    df_agg_ajc = aggregate_by_topic(ajc, 'AJC')
    df_agg_latimes = aggregate_by_topic(latimes, "LA Times")
    df_agg_denver_post = aggregate_by_topic(denver_post, "Denver Post")
    df_agg_ajc_group = aggregate_by_topic(ajc, 'AJC','group')
    df_agg_latimes_group = aggregate_by_topic(latimes, "LA Times", 'group')
    df_agg_denver_post_group = aggregate_by_topic(denver_post, "Denver Post", 'group')

    df_all_sources = df_agg_ajc.append(df_agg_latimes, ignore_index=True)
    df_all_sources = df_all_sources.append(df_agg_denver_post, ignore_index=True)

    # create plots for each topic label showing all three sources
    topic_labels = df_agg_all['topic_label']
   # for topic in topic_labels:
   #     bubble_by_source_by_topic(df_all_sources, topic)

    # Create bubble for all topics not by source
    df_agg_all_top10 = df_agg_all.sort(['topic_count'], ascending=False)[0:10]
    all_topics_bubble(df_agg_all_top10)

    bar_ratio_chart(df_agg_all.sort(['ratio'], ascending=False))
    #create dataframe dropping the groups don't want to show
    to_keep = ['Lifestyle', 'Politics', 'Business', 'Crime', 'Education', 'Real Estate', 'Sports']
    df_agg_all_keygroups = df_agg_all_group[df_agg_all_group['group'].isin(to_keep)]

    bubble_ratio_chart(df_agg_all_group.sort(['ratio'], ascending=False), level='group', title='keygroups')


    #Same groups by source
    df_agg_ajc_keygroups = df_agg_ajc_group[df_agg_ajc_group['group'].isin(to_keep)]
    df_agg_denver_post_keygroups = df_agg_denver_post_group[df_agg_denver_post_group['group'].isin(to_keep)]
    df_agg_latimes_keygroups = df_agg_latimes_group[df_agg_latimes_group['group'].isin(to_keep)]

    #Need to create a 'dummy' group that represents order in which to display topics
    df_agg_ajc_keygroups['dummy_group'] = df_agg_ajc_keygroups.apply(lambda row: create_dummy_groups(row), axis=1)
    df_agg_denver_post_keygroups['dummy_group'] = df_agg_denver_post_keygroups.apply(lambda row: create_dummy_groups(row), axis=1)
    df_agg_latimes_keygroups['dummy_group'] = df_agg_latimes_keygroups.apply(lambda row: create_dummy_groups(row), axis=1)

    bubble_ratio_chart_by_source(df_agg_ajc_keygroups, df_agg_latimes_keygroups, df_agg_denver_post_keygroups, level='group', title='keygroups')


    #group 1
    group1 = ['Arts/Cultural', 'Books', 'Entertainment', 'Food', 'Gardening',
              'Lifestyle', 'Music']
    df_agg_ajc_1 = df_agg_ajc[df_agg_ajc['topic_label'].isin(group1)]
    df_agg_latimes_1 = df_agg_latimes[df_agg_latimes['topic_label'].isin(group1)]
    df_agg_denver_post_1 = df_agg_denver_post[df_agg_denver_post['topic_label'].isin(group1)]
    bubble_ratio_chart_by_source(df_agg_ajc_1, df_agg_latimes_1, df_agg_denver_post_1, title='1')

    #group2
    global group2
    group2 = ['U.S. Politics', 'Local Politics/Government', 'International']
    df_agg_ajc_2 = df_agg_ajc[df_agg_ajc['topic_label'].isin(group2)]
    df_agg_latimes_2 = df_agg_latimes[df_agg_latimes['topic_label'].isin(group2)]
    df_agg_denver_post_2 = df_agg_denver_post[df_agg_denver_post['topic_label'].isin(group2)]
    bubble_ratio_chart_by_source(df_agg_ajc_2, df_agg_latimes_2, df_agg_denver_post_2, title='2')

    #group3
    global group3
    group3 = ['Business', 'Crime', 'Education', 'Real Estate']
    df_agg_ajc_3 = df_agg_ajc[df_agg_ajc['topic_label'].isin(group3)]
    df_agg_latimes_3 = df_agg_latimes[df_agg_latimes['topic_label'].isin(group3)]
    df_agg_denver_post_3 = df_agg_denver_post[df_agg_denver_post['topic_label'].isin(group3)]
    bubble_ratio_chart_by_source(df_agg_ajc_3, df_agg_latimes_3, df_agg_denver_post_3, title='3')
