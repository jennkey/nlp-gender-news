import plotly.plotly as py
import plotly
import plotly.graph_objs as go
import pandas as pd


def all_topics_bubble(df_agg):
    # Data for source 1
    trace0 = go.Scatter(
      x=df_agg['female_percent'],
      y=df_agg['male_percent'],
      text=df_agg['topic_label'],
      mode='markers+text',
      marker=dict(
          size=df_agg['topic_count'],
          color=['rgb(93, 164, 214)'],
          sizemode='area',
          sizeref=1,
      ),
      textposition = 'center'
    )

    trace1 = go.Scatter(
        x=[0,.1,.2,.3,.4,.5,.6,.7,.8,.9,1, 1.1, 1.2],
        y=[0,.1,.2,.3,.4,.5,.6,.7,.8,.9,1, 1.1, 1.2]
    )

    data = [trace0, trace1]

    layout = go.Layout(
        title="Ratio Male to Female Sentences: All Sources",
        showlegend=False,
        autosize=True)
    fig = go.Figure(data=data, layout=layout)

    plot_filename = "/Users/jenniferkey/galvanize/nlp-gender-news/plots/bubblechart_all_topics.html"
    plotly.offline.plot(fig, filename=plot_filename)
