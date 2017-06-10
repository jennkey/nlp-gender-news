import matplotlib.pyplot as plt

def aggregate_by_topic(df_unagg):
    df_agg = df_unagg[['topic', 'male_sentences', 'both_sentences', 'female_sentences']].groupby(['topic']).sum()
    df_agg['topic_count'] = df_unagg[['topic']].groupby(['topic']).size()
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

    y = df_agg['male_percent']
    x = df_agg['female_percent']
    s = df_agg['topic_count']

    f, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(x,y,s=s)
    ax.set(xlim=(0, 1), ylim=(0, 1))

    # Plot your initial diagonal line based on the starting
    # xlims and ylims.
    diag_line, = ax.plot(ax.get_xlim(), ax.get_ylim(), ls="--", c=".3")
    # Connect two callbacks to your axis instance.
    # These will call the function "on_change" whenever
    # xlim or ylim is changed.
    ax.callbacks.connect('xlim_changed', on_change)
    ax.callbacks.connect('ylim_changed', on_change)
