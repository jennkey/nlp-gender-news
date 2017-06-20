import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from adjustText import adjust_text

def aggregate_by_topic(df_unagg):
    df_agg = df_unagg[['topic_label', 'male_sentences', 'both_sentences', 'female_sentences']].groupby(['topic_label']).sum()
    df_agg['topic_count'] = df_unagg[['topic_label']].groupby(['topic_label']).size()
    print(df_agg)
    return df_agg

def on_change(axes):
    # When this function is called it checks the current
    # values of xlim and ylim and modifies diag_line
    # accordingly.
    x_lims = ax.get_xlim()
    y_lims = ax.get_ylim()
    diag_line.set_data(x_lims, y_lims)

def gender_bubble_plot(df_unagg):
    '''
    Creates a bubble plot showing the percent of male sentences
    on y axis, percent of female sentences on x axis,
    and number of documents as Size

    Inputs: df_unagg = unaggregated data frame
            outplot = name of file to output graph to
    '''

    df_agg = aggregate_by_topic(df_unagg)

    count_all_sentences = df_agg['male_sentences'] + df_agg['female_sentences'] + df_agg['both_sentences']
    df_agg['male_percent'] = (df_agg['male_sentences'] + df_agg['both_sentences'])/count_all_sentences
    df_agg['female_percent'] = (df_agg['female_sentences'] + df_agg['both_sentences'])/ count_all_sentences
    df_agg.reset_index(level=0, inplace=True)

    N = len(df_agg)
    y = df_agg['male_percent']
    x = df_agg['female_percent']
    s = df_agg['topic_count']*4
    topic = df_agg.iloc[:,0]
    # Choose some random colors
    colors=cm.rainbow(np.random.rand(N))


    f, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(x,y,s=s, cmap='rainbow', alpha=.5)
    ax.set(xlim=(0, 1), ylim=(0, 1),
        title="Los Angeles Times",
        xlabel='Percent of Female Sentences',
        ylabel='Percent of Male Sentences')
     # plotting the first eigth letters of the state's name
    #text(y, y,
      #topic ,size=11,horizontalalignment='center')
    texts = []
    for x_p, y_p, text in zip(x, y, topic):
        texts.append(ax.text(x_p, y_p, text))
    adjust_text(texts, force_text=0.05, arrowprops=dict(arrowstyle="->",
                                                    color='r', alpha=0.5))
    # for i in range(N):
    #      ax.annotate(topic[i], xy=(x.iat[i],y.iat[i]),
    #                  xytext=pos[ano_str], textcoords='data',
    #                  arrowprops=dict(arrowstyle="->",
    #                             connectionstyle="arc3"))

    #ax.legend(loc='best')

    # Plot your initial diagonal line based on the starting
    # xlims and ylims.
    diag_line, = ax.plot(ax.get_xlim(), ax.get_ylim(), ls="--", c='grey')
    # Connect two callbacks to your axis instance.
    # These will call the function "on_change" whenever
    # xlim or ylim is changed.
    ax.callbacks.connect('xlim_changed', on_change)
    ax.callbacks.connect('ylim_changed', on_change)
    return df_agg
