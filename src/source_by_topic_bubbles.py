import plotly.plotly as py
import plotly
import plotly.graph_objs as go
import pandas as pd

#df_agg = pd.read_pickle('/Users/jenniferkey/galvanize/nlp-gender-news/data/all/df_agg.pkl')




def bubble_by_source_by_topic(df_agg_ajc, df_agg_latimes, df_agg_denver_post, topic_label):
    # create dataframe with only those articles from given topic_label
    print('Topic Label{}'.format(topic_label))
    #subset datasets

    # Data for source 1
    trace1 = go.Scatter(
        x = [.4, .8]
        y = [.5, .9]
        #x=df_agg_ajc['female_percent'][df_agg_ajc['topic_label'] == topic_label].values,
        #y=df_agg_ajc['male_percent'][df_agg_ajc['topic_label'] == topic_label].values,
        mode='markers',
        # text=df_agg_ajc['topic_label'][df_agg_ajc['topic_label'] == topic_label].values[0],
        marker=dict(
            size = [10,10]
            #size=df_agg_ajc['topic_count'][df_agg_ajc['topic_label'] == topic_label].values,
            sizeref=20,
            sizemode='area',
            color=['rgb(93, 164, 214)']
        ),
        # textposition=["middle left","top center","bottom center"],
        # textfont=dict(
        #     color = "#bebada",
        #     family='sans serif',
        #     size=18,
        # )
    )

    # Data for source 2
    trace2 = go.Scatter(
        x=df_agg_latimes['female_percent'][df_agg_latimes['topic_label'] == topic_label].values,
        y=df_agg_latimes['male_percent'][df_agg_latimes['topic_label'] == topic_label].values,
        mode='markers',
        text=df_agg_latimes['topic_label'][df_agg_latimes['topic_label'] == topic_label].values,
        marker=dict(
            size=df_agg_latimes['topic_count'][df_agg_latimes['topic_label'] == topic_label].values,
            sizeref=20,
            sizemode='area',
            color=['rgb(255, 144, 14)']
        ),
        textposition=["middle left","top center","bottom center"],
        textfont=dict(
            color = "#bebada",
            family='sans serif',
            size=18,
        )
    )

    # Data for source 3
    trace3 = go.Scatter(
        x=[df_agg_denver_post['female_percent'][df_agg_denver_post['topic_label'] == topic_label].values[0]],
        y=[df_agg_denver_post['male_percent'][df_agg_denver_post['topic_label'] == topic_label].values[0]],
        mode='markers',
        marker=dict(
            size=[df_agg_denver_post['topic_count'][df_agg_denver_post['topic_label'] == topic_label].values[0]]
        ),
    )
    #Diagonal Line
    trace4 = go.Scatter(
        x=[0,.1,.2,.3,.4,.5,.6,.7,.8,.9,1, 1.1, 1.2],
        y=[0,.1,.2,.3,.4,.5,.6,.7,.8,.9,1, 1.1, 1.2]
    )
    data = [trace1, trace2, trace3, trace4]
    layout = go.Layout(
        xaxis=dict(
            range=[0, 1]
        ),
        yaxis=dict(
            range=[0, 1]
        )
    )
    plot_filename = "/Users/jenniferkey/galvanize/nlp-gender-news/plots/bubblechart_{}.html".format(topic_label)
    plotly.offline.plot(data, filename=plot_filename)
