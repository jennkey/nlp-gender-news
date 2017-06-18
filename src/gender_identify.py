from __future__ import division

import glob
import nltk
from string import punctuation
import pandas as pd
import numpy as np
import unicodedata
import re
import string
import matplotlib.pyplot as plt
from gender_bubble_plot import gender_bubble_plot
from collections import Counter
from nltk.corpus import stopwords
import sys


tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')


#Two lists  of words that are used when a man or woman is present, based on Danielle Sucher's https://github.com/DanielleSucher/Jailbreak-the-Patriarchy
male_words=set(['guy','spokesman','chairman',"men's",'men','him',"he's",'his','boy','boyfriend','boyfriends','boys','brother','brothers','dad','dads','dude','father','fathers','fiance','gentleman','gentlemen','god','grandfather','grandpa','grandson','groom','he','himself','husband','husbands','king','male','man','mr','nephew','nephews','priest','prince','son','sons','uncle','uncles','waiter','widower','widowers'
'hes', 'mens', 'mans'])
female_words=set(['heroine','spokeswoman','chairwoman',"women's",'actress','women',"she's",'her','aunt','aunts','bride','daughter','daughters','female','fiancee','girl','girlfriend','girlfriends','girls','goddess','granddaughter','grandma','grandmother','herself','ladies','lady','lady','mom','moms','mother','mothers','mrs','ms','niece','nieces','priestess','princess','queens','she','sister','sisters','waitress','widow','widows','wife','wives','woman', 'shes', 'womans', 'womens'])

# function to read records from mongo db
def read():
    df = pd.DataFrame(list(db.articles.find()))
    return df

def clean_text(text):
    # remove 'by author'
    text = text.replace(r"By[^,]*","")
    # change contractions to their long form
    text = text.replace(r"what's", "what is ")
    text = text.replace(r"what's", "what is ")
    text = text.replace(r"\\u2019s", " ")
    text = text.replace(r"\'ve", " have ")
    text = text.replace(r"can't", "cannot ")
    text = text.replace(r"n\\u2019t", " not ")
    text = text.replace(r"i'm", "i am ")
    text = text.replace(r"\'re", " are ")
    text = text.replace(r"\'d", " would ")
    text = text.replace(r"\'ll", " will ")
    text = text.replace(r"2019", "")
    text = text.replace(r"201d", "")

    #text = unicodedata.normalize('NFKD', text).encode('ascii','ignore')

    return text

def gender_the_sentence(sentence_words):
    mw_length=len(male_words.intersection(sentence_words))
    fw_length=len(female_words.intersection(sentence_words))

    if mw_length>0 and fw_length==0:
        gender='male'
    elif mw_length==0 and fw_length>0:
        gender='female'
    elif mw_length>0 and fw_length>0:
        gender='both'
    else:
        gender='none'
    return gender

def is_it_proper(word):
    if word[0]==word[0].upper():
        case='upper'
    else:
        case='lower'

    word_lower=word.lower()
    try:
        proper_nouns[word_lower][case] = proper_nouns[word_lower].get(case,0)+1
    except:
        #This is triggered when the word hasn't been seen yet
        proper_nouns[word_lower]= {case:1}


def increment_gender(sentence_words,gender):
    sentence_counter[gender]+=1
    # get the number of words in sentence by sex
    word_counter[gender]+=len(sentence_words)
    # get the number of times each word appears in the sentence
    # May add stop words and lemmatizer here?
    for word in sentence_words:
        word_freq[gender][word]=word_freq[gender].get(word,0)+1


def top_male_female_words_by_topic(df):
    unique_topics = df['topic_label'].unique()
    for topic in unique_topics:
        female_words_to_count = df['female_word_count'][(df['topic_label'] == topic)]
        total_female_words = df['total_female_words'][(df['topic_label'] == topic)].sum()
        female_words_dict = Counter({})
        for word_dict in female_words_to_count:
            female_words_dict = female_words_dict + Counter(word_dict)

        male_words_to_count = df['male_word_count'][(df['topic_label'] == topic)]
        total_male_words = df['total_male_words'][(df['topic_label'] == topic)].sum()
        male_words_dict = Counter({})

        for word_dict in male_words_to_count:
            male_words_dict = male_words_dict + Counter(word_dict)


        # Create a set of words that appear in both male and female sentences
        common_words=set([w for w in sorted(female_words_dict, key=female_words_dict.get, reverse=True)[:1000]]+[w for w in sorted (male_words_dict, key=male_words_dict.get, reverse=True)[:1000]])
        #remove gendered words, stop words
        #common_words=list(common_words-male_words-female_words-proper_nouns_set)
        common_words=list(common_words-male_words-female_words-stop_set-proper_nouns_set)

        #Find words that are frequent but most unique
        female_percent= {word: (float(female_words_dict.get(word,0)) / float(total_female_words) / (float(female_words_dict.get(word,0)) / float(total_female_words) +
        (float(male_words_dict.get(word,0) / float(total_male_words))))) for word in common_words
         if female_words_dict.get(word,0) > 5}

        male_percent= {word: (float(male_words_dict.get(word,0)) / float(total_male_words) / (float(male_words_dict.get(word,0)) / float(total_male_words) +
        (float(female_words_dict.get(word,0) / float(total_female_words))))) for word in common_words
        if male_words_dict.get(word,0) > 5}

        print()
        print("Topic: ", topic, "Female Words")
        print("word", "ratio", "male count", "female count")
        for word in sorted (female_percent, key=female_percent.get, reverse=True)[:50]:
            try:
                ratio = float(female_percent[word])/float((1-female_percent[word]))
            except:
                ratio = 100
            print(word, ratio, male_words_dict.get(word,0), female_words_dict.get(word,0) )

        print
        print("Topic", topic, "Male Words")
        print("word", "ratio", "male count", "female count")
        for word in sorted (male_percent, key=male_percent.get, reverse=True)[:50]:
            try:
                ratio = float(male_percent[word])/float((1-male_percent[word]))
            except:
                ratio = 100
            print(word, ratio, male_words_dict.get(word,0), female_words_dict.get(word,0) )


        #print (female_percent)
         #     header ='Ratio\tMale\tFemale\tWord'
         #     print 'Male words'
         #     print header
         #     for word in sorted (male_percent,key=male_percent.get,reverse=True)[:20]:
         #         try:
         #             ratio=male_percent[word]/(1-male_percent[word])
         #         except:
         #             ratio=100
                 #print '%.1f\t%02d\t%02d\t%s' % (ratio,word_freq['male'].get(word,0),word_freq['female'].get(word,0),word)
         #         print(ratio,word_freq['male'].get(word,0),word_freq['female'].get(word,0),word)
         #         male_words_ = (word, word_freq['male'].get(word,0), word_freq['female'].get(word,0))
         #
         # if word_counter['female'] > 0:
         #     print '\n'*2
         #     print 'Female words'
         #     print header
         #     for word in sorted (male_percent,key=male_percent.get,reverse=False)[:20]:
         #         try:
         #             ratio=(1-male_percent[word])/male_percent[word]
         #         except:
         #             ratio=100
         #         #print '%.1f\t%01d\t%01d\t%s' % (ratio,word_freq['male'].get(word,0),word_freq['female'].get(word,0),word)
         #         print(ratio,word_freq['male'].get(word,0),word_freq['female'].get(word,0),word)
         #         female_words_ = (word, word_freq['male'].get(word,0), word_freq['female'].get(word,0))


#         for
#         frequencies = [val /freq_sum for val in H_nmf[topic_indx]]
#     return dict(zip(tfidf_feature_names, frequencies))

if __name__ == '__main__':

    #read in newspaper
    news_paper = sys.argv[1]

    # Create paths for data and plots
    datapath = '/Users/jenniferkey/galvanize/nlp-gender-news/data/{}/'.format(news_paper)
    plotpath = '/Users/jenniferkey/galvanize/nlp-gender-news/plots/{}/'.format(news_paper)

    # read in pickled dataframe with topics and labels
    topics_file = datapath + 'topic_labeled.pkl'
    df = pd.read_pickle(topics_file)
    #df['article'] = df['article'].apply(lambda x: ', '.join(x))
    text = df['article']

    #file_list='articles/*.txt')
    #Open the file
    #text=open(file_name,'rb').read()


    #filtered_string = filter(lambda x: x in string.printable, myStr)
    count = 0
    male_sentences_list = []
    female_sentences_list = []
    both_sentences_list = []
    none_sentences_list = []
    female_word_count_list = []
    male_word_count_list = []
    total_female_word_count = []
    total_male_word_count = []
    stop_set = set(stopwords.words('english'))
    stop_set.update(['said', 'say', 'thing', 'know', 'like'])

    for article in text:

        # initialize a few variables
        sexes=['male','female','none','both']
        # Sentence_counter is a dictionary with key for all 'sexes' in list
        # and value will be the count of the number of sentences that
        #  are that 'sex'
        sentence_counter={sex:0 for sex in sexes}
        # word_counter is a dictionary with each 'sex' from sex list as
        # the key and the number of words in the sentence as the value
        word_counter={sex:0 for sex in sexes}
        # word_freq is a dictionary with the sexes as the key and then a
        # dictionary of words with their count as the value
        word_freq={sex:{} for sex in sexes}
        proper_nouns={}

        #Not sure I need this anymore test it
        article = filter(lambda x: x in string.printable, article)

        #Split into sentences
        sentences=tokenizer.tokenize(article)

        for sentence in sentences:
            #word tokenize and strip punctuation
            sentence_words = clean_text(sentence)
            sentence_words=sentence.split()

            sentence_words=[w.strip(punctuation) for w in sentence_words if len(w.strip(punctuation))>0]

            #figure out how often each word is capitalized
            [is_it_proper(word) for word in sentence_words[1:]]

            #lower case it
            sentence_words=set([w.lower() for w in sentence_words])

            #Figure out if there are gendered words in the sentence by computing the length of the intersection of the sets
            gender=gender_the_sentence(sentence_words)

            #Increment some counters
            increment_gender(sentence_words,gender)

        proper_nouns_set=set([word for word in proper_nouns if
                          proper_nouns[word].get('upper',0) /
                          (proper_nouns[word].get('upper',0) +
                           proper_nouns[word].get('lower',0))>.50])


        #remove gendered words, stop words
        #common_words=list(common_words-male_words-female_words-proper_nouns_set)
       # common_words=list(common_words-male_words-female_words)

        count += 1

        # set counts of male sentences, female sentences, both and none per article
        # to lists
        male_sentences = sentence_counter['male']
        female_sentences = sentence_counter['female']
        both_sentences = sentence_counter['both']
        none_sentences = sentence_counter['none']

        male_sentences_list.append(male_sentences)
        female_sentences_list.append(female_sentences)
        both_sentences_list.append(both_sentences)
        none_sentences_list.append(none_sentences)

        # print '%.1f sentences about men for each sentence about women.' % ((sentence_counter['male'] + .0000001) /(sentence_counter['female'] + .0000001))

        # Create dictionary of female words
        # Create dictionary of male words
        # append the dictionaries to list for all articles
        female_word_count_list.append(word_freq['female'])
        male_word_count_list.append(word_freq['male'])

        # create list of total female and male words
        total_female_word_count.append(word_counter['female'])
        total_male_word_count.append(word_counter['male'])



        #Create dicitonary of most frequent male words
       #

    #appending metrics to DataFrame
    df['male_sentences'] = male_sentences_list
    df['female_sentences'] = female_sentences_list
    df['both_sentences'] = both_sentences_list
    df['none_sentences'] = none_sentences_list
    df['total_female_words'] = total_female_word_count
    df['total_male_words'] = total_male_word_count
    df['female_word_count'] = female_word_count_list
    df['male_word_count'] = male_word_count_list


    #f, ax = plt.subplots(figsize=(6, 6))
    df_agg = gender_bubble_plot(df)
    file_name = plotpath + 'gender_bubble_plot.png'
    plt.savefig(file_name, dpi=250)
    plt.close()

    #top_male_female_words_by_topic(df)

    # Save the pickled dataframe for easy access later
    agg_file = datapath + 'df_agg.pkl'
    df_agg.to_pickle(agg_file)
    gendered_articles = datapath + 'df_gendered_articles.pkl'
    df.to_pickle(gendered_articles)
