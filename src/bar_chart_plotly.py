def bar_chart():
    # trace1 = go.Bar(
    #     x=news_papers,
    #     y=ratio_male_to_female_articles_list,
    #     name='Articles: Male to Female Ratio'
    # )
    #
    #     plotly.offline.plot(data, filename='bubblechart-size.html')
    #
    # trace2 = go.Bar(
    #     x=news_papers,
    #     y=ratio_male_to_female_sentences_list,
    #     name='Sentences: Male to Female Ratio'
    # )
    #
    # data = [trace1, trace2]
    #layout = go.Layout(
    #    barmode='group'
    #)
    trace0 = go.Bar(
        x=pretty_names,
        y=ratio_male_to_female_articles_list,
        marker=dict(
            color=[ '#68829E', '#AEBD38', "#598234",]
            )
        )
    trace1 = go.Bar(
        x=pretty_names,
        y=ratio_male_to_female_sentences_list,
        marker=dict(
            color=[ '#68829E', '#AEBD38', "#598234",],
            )
        )

    layout = dict(
        title='Male to Female Ratios',
        yaxis1=dict(
            range=[0,4],
            showgrid=False,
            showline=False,
            showticklabels=True,
            domain=[0, 0.85],
        ),
        yaxis2=dict(
            range=[0,4],
            showgrid=False,
            showline=True,
            showticklabels=False,
            linewidth=2,
            domain=[0, 0.85],
        ),
        xaxis1=dict(
            zeroline=False,
            showline=False,
            showticklabels=True,
            showgrid=True
        ),
        xaxis2=dict(
            zeroline=False,
            showline=False,
            showticklabels=True,
            showgrid=True
        ),
        margin=dict(
            l=100,
            r=20,
            t=70,
            b=70,
        ),

        paper_bgcolor='rgb(248, 248, 255)',
        plot_bgcolor='rgb(248, 248, 255)',
        showlegend=false
    )
    annotations = []

    ratio_s = np.round(ratio_male_to_female_sentences_list, decimals=2)
    ratio_a = np.round(ratio_male_to_female_articles_list, decimals=2)
    print(ratio_s)
    print(ratio_a)

    # Adding labels
    for ys, ya, xd in zip(ratio_s, ratio_a, pretty_names):
        # labeling  bar chart articles
        annotations.append(dict(xref='x1', yref='y1',
                                y=ya+.1, x=xd,
                                text=str(ya),
                                font=dict(family='Arial', size=12,
                                          color=[ '#68829E', '#AEBD38', "#598234",]),
                                showarrow=False))
        # labeling the bar chart sentences
        annotations.append(dict(xref='x2', yref='y2',
                                y=ys+.1, x=xd,
                                text=str(ys),
                                font=dict(family='Arial', size=12,
                                          color=[ '#68829E', '#AEBD38', "#598234",]),
                                showarrow=False))

    layout['annotations'] = annotations
    # Creating two subplots
    fig = tools.make_subplots(rows=1, cols=2,  shared_xaxes=False,
                              shared_yaxes=False, vertical_spacing=0.001,
                              subplot_titles=('Articles', 'Sentences'))

    fig.append_trace(trace0, 1, 1)
    fig.append_trace(trace1, 1, 2)

    fig['layout'].update(layout)

    plotly.offline.plot(fig, filename='ratios.html')
