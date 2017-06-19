import plotly.plotly as py
import plotly
import plotly.graph_objs as go
import pandas as pd


def bar_ratio_chart(df_agg):

    trace0 = go.Bar(
        x=df_agg['topic_label'],
        y=df_agg['ratio'],
        marker=dict(
            color=[ '#68829E']
            )
     )

    data = [trace0]
    plot_filename = "/Users/jenniferkey/galvanize/nlp-gender-news/plots/topics.html"
    plotly.offline.plot(data, filename=plot_filename)

def bubble_ratio_chart(df_agg):
    df_agg.sort(['ratio'], ascending=True)
    trace0 = go.Scatter(
        y=df_agg['topic_label'],
        x=df_agg['ratio'],
        mode='markers',
        marker=dict(
            size=df_agg['topic_count'],
            color=['rgb(93, 164, 214)'],
            sizemode='area',
            sizeref=1,
            )

     )

    trace1 = go.Scatter(
        y=df_agg['topic_label'],
        x=[1 for e in range(0,len(df_agg))],
    )

    layout = go.Layout(
        title="Ratio Male to Female Sentences: All Sources",
        showlegend=False,
        autosize=False,
        width=1000,
        height=600,
        margin=go.Margin(
        l=200,
        r=50,
        b=50,
        t=50,
        pad=10),
        yaxis=dict(
           autorange='reversed'),
       
    )

    data = [trace0, trace1]
    fig = go.Figure(data=data, layout=layout)
    plot_filename = "/Users/jenniferkey/galvanize/nlp-gender-news/plots/bubbles_topics.html"
    plotly.offline.plot(fig, filename=plot_filename)
