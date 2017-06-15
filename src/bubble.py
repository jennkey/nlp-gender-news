import plotly.plotly as py
import plotly
import plotly.graph_objs as go
import pandas as pd

df_agg_latimes = pd.read_pickle('/Users/jenniferkey/galvanize/nlp-gender-news/data/latimes/df_agg.pkl')
df_agg_denpost = pd.read_pickle('/Users/jenniferkey/galvanize/nlp-gender-news/data/denver_post/df_agg.pkl')

df_agg_latimes.sort_values(['male_percent', 'female_percent'], ascending=[True, True], inplace=True)
df_agg_denpost.sort_values(['male_percent', 'female_percent'], ascending=[True, True], inplace=True)



trace1 = go.Scatter(
    x=df_agg_denpost['female_percent'],
    y=df_agg_denpost['male_percent'],
    mode='markers+text',
    text=df_agg_denpost['topic_label'],
    marker=dict(
        size=df_agg_denpost['topic_count'],
        sizeref=0.2,
        sizemode='area',
        color = "#bebada"
    ),
    textposition=["middle left","top center","bottom center","top right","middle left"],
    textfont=dict(
        color = "#bebada",
        family='sans serif',
        size=18,
    )
)

trace2 = go.Scatter(
    x=df_agg_latimes['female_percent'],
    y=df_agg_latimes['male_percent'],
    mode='markers+text',
    text=df_agg_latimes['topic_label'],
    marker=dict(
        size=df_agg_latimes['topic_count'],
        sizeref=0.2,
        sizemode='area',
        color="#fdb462"
    ),
    textposition=['bottom left', 'bottom center', 'top center', 'bottom right', 'middle right'],
    textfont=dict(
        color = "#fdb462",
        family='sans serif',
        size=18,
    )
)

trace3 = go.Scatter(
    x=[0,.1,.2,.3,.4,.5,.6,.7,.8,.9,1, 1.1, 1.2],
    y=[0,.1,.2,.3,.4,.5,.6,.7,.8,.9,1, 1.1, 1.2]
)

data = [trace1, trace2, trace3]
layout = go.Layout(
    xaxis=dict(
        range=[0, 1]
    ),
    yaxis=dict(
        range=[0, 1]
    )
)
plotly.offline.plot(data, filename='bubblechart-size.html')
