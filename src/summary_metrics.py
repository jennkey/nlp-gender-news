import pandas as pd

# creates summary metrics for all sources

def read_pickle_df(news_paper):
    '''
    Reads in pickled dataframe for each newspaper
    '''
    datapath = '/Users/jenniferkey/galvanize/nlp-gender-news/data/{}/'.format(news_paper)
    pickle_to_read = datapath + 'df_gendered_articles.pkl'
    df = pd.read_pickle(pickle_to_read)
    return df

def summary_metrics(news_paper):
    '''
    Creates summary metrics for each newspaper
    '''
    #overall ratio of male sentences to female sentences
    ratio_male_to_female_sentences_list.append(float(df['male_sentences'].sum() + df['both_sentences'].sum()) / float(df['female_sentences'].sum() + df['both_sentences'].sum()))

    male_articles = len(df[(df['female_sentences'] < df['male_sentences'])])
    print(male_articles)
    female_articles = len(df[(df['female_sentences'] > df['male_sentences'])])
    print(female_articles)
    ratio_male_to_female_articles_list.append(float(male_articles)/float(female_articles))




if __name__ == '__main__':
    news_papers = ['ajc']
    ratio_male_to_female_articles_list = []
    ratio_male_to_female_sentences_list = []
    # read in pickled dataframe with topics and labels
    for newspaper in news_papers:
        df = read_pickle_df(newspaper)
        summary_metrics(newspaper)
