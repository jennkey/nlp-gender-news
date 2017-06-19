import plotly.plotly as py
import plotly
import plotly.graph_objs as go
import pandas as pd

#df_agg = pd.read_pickle('/Users/jenniferkey/galvanize/nlp-gender-news/data/all/df_agg.pkl')




def bubble_by_source_by_topic(df_agg, topic_label):
    # create dataframe with only those articles from given topic_label
    print('Topic Label{}'.format(topic_label))



    # Data for source 1
    trace0 = go.Scatter(
        x=df_agg['female_percent'][df_agg['topic_label'] == topic_label],
        y=df_agg['male_percent'][df_agg['topic_label'] == topic_label],
        text=['AJC', 'LA Times', 'Denver Post'],
        mode='markers+text',
        marker=dict(
            size=df_agg['topic_count'][df_agg['topic_label'] == topic_label],
            color=['rgb(93, 164, 214)', 'rgb(255, 144, 14)',  'rgb(44, 160, 101)'],
            sizemode='area',
            sizeref=.02,
        ),
        textposition = 'top'
    )

    trace1 = go.Scatter(
        x=[0,.1,.2,.3,.4,.5,.6,.7,.8,.9,1],
        y=[0,.1,.2,.3,.4,.5,.6,.7,.8,.9,1],
        mode = 'lines',
    )

    data = [trace0, trace1]

    layout = go.Layout(
        title=topic_label,
        showlegend=False,
        autosize=False,
        width=500,
        height=500,)
    fig = go.Figure(data=data, layout=layout)

    # create file name based on the topic, but need to remove '/'
    plot_name = topic_label.replace('/','')
    plot_filename = "/Users/jenniferkey/galvanize/nlp-gender-news/plots/bubblechart_{}.html".format(plot_name
)
    plotly.offline.plot(fig, filename=plot_filename)
