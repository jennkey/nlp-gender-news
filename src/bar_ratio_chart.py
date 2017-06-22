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

def bubble_ratio_chart(df_agg, level='topic_label', title='none'):
    global max_x
    max_x = max(df_agg['ratio']) + 2
    df_agg.sort(['ratio'], ascending=True)
    trace0 = go.Scatter(
        y=df_agg[level],
        x=df_agg['ratio'],
        mode='markers',
        marker=dict(
            size=df_agg['topic_count'],
            #color=['rgb(93, 164, 214)'],
            color=['#800000' for e in range(0,len(df_agg))],
            sizemode='area',
            sizeref=.5,
            )

     )

    trace1 = go.Scatter(
        y=df_agg[level],
        x=[1 for e in range(0,len(df_agg))],
        mode = 'lines',
        name = '1:1',
        line = dict(
            color = ('#006400'),
            width = 2,
            dash = 'dash')
    )

    trace2 = go.Scatter(
        y=df_agg[level],
        x=[3.61 for e in range(0,len(df_agg)+1)],
        mode='lines',
        name = 'Overall 3.61 Male to Female Sentences',
        line = dict(
            color = ('#FF4500'),
            width = 2,
            dash = 'dash')
    )

    layout = go.Layout(
        #title="Ratio Male to Female Sentences: All Sources",
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
           #title='Ratio Male Sentences to Female Sentences',
           autorange='reversed',
           tickfont=dict(
               family='Heuristica',
               size=26,
               color='black')),
        xaxis=dict(zeroline=True, range=[0, max_x],
                       tickfont=dict(
                       family='Heuristica',
                       size=24,
                       color='black'))
    )

    data = [trace0, trace1, trace2]
    fig = go.Figure(data=data, layout=layout)
    plot_filename = "/Users/jenniferkey/galvanize/nlp-gender-news/plots/bubbles_topics_{}.html".format(title)
    plotly.offline.plot(fig, filename=plot_filename)


def bubble_ratio_chart_by_source(df_agg_ajc, df_agg_latimes, df_agg_denver_post, group):
    #max_x = max(max(df_agg_ajc['ratio']), max(df_agg_latimes['ratio']), max(df_agg_denver_post['ratio'])) + 1
    trace0 = go.Scatter(
        y=df_agg_ajc['topic_label'],
        x=df_agg_ajc['ratio'],
        mode='markers',
        marker=dict(
            size=df_agg_ajc['topic_count'],
            color=['#9400D3' for e in range(0,len(df_agg_ajc))],
            sizemode='area',
            sizeref=.25,
            ),
        name="AJC"

     )
    trace1 = go.Scatter(
         y=df_agg_latimes['topic_label'],
         x=df_agg_latimes['ratio'],
         mode='markers',
         marker=dict(
             size=df_agg_latimes['topic_count'],
             color=['#FF4500' for e in range(0,len(df_agg_ajc))],
             sizemode='area',
             sizeref=.1,
             ),
          name="LA Times"

      )
    trace2 = go.Scatter(
        y=df_agg_denver_post['topic_label'],
        x=df_agg_denver_post['ratio'],
        mode='markers',
        marker=dict(
            size=df_agg_denver_post['topic_count'],
            color=['#2F4F4F' for e in range(0,len(df_agg_ajc))],
            sizemode='area',
            sizeref=.1,
            ),
        name="Denver Post"

     )
    trace3 = go.Scatter(
        y=df_agg_ajc['topic_label'],
        x=[1 for e in range(0,len(df_agg_ajc))],
        mode = 'lines',
        name = '1:1',
        line = dict(
            color = ('#006400'),
            width = 2,
            dash = 'dash'),
        showlegend=False
    )

    trace4 = go.Scatter(
        y=df_agg_ajc['topic_label'],
        x=[3.61 for e in range(0,len(df_agg_ajc)+1)],
        mode='lines',
        name = 'Overall 3.61 Male to Female Sentences',
        line = dict(
            color = ('#FF4500'),
            width = 2,
            dash = 'dash'),
        showlegend=False
    )

    layout = go.Layout(
        #title="Ratio Male to Female Sentences: All Sources",
        showlegend=True,
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
           #title='Ratio Male Sentences to Female Sentences',
           autorange='reversed',
           tickangle=45,
           tickfont=dict(
               family='Heuristica',
               size=24,
               color='black',
           ),
        ),
       xaxis=dict(zeroline=True,range=[0, max_x],
           tickfont=dict(
               family='Heuristica',
               size=24,
               color='black'
           )),
       legend=dict(
        x=80,
        y=1,
        traceorder='normal',
        font=dict(
            family='Heuristica',
            size=24,
        )),
       )


    data = [trace0, trace1, trace2, trace3, trace4]
    fig = go.Figure(data=data, layout=layout)
    plot_filename = "/Users/jenniferkey/galvanize/nlp-gender-news/plots/bubbles_topics_sources_{}.html".format(group)
    plotly.offline.plot(fig, filename=plot_filename)
