import plotly.graph_objs as go
from plotly.offline import plot

#graph for cltv
def graph_cltv():
    data = [go.Bar(
        x=[1, 6, 20, 400, 10, 1000],
        y=['Minimum', 'First_quartile', 'Median', 'Mean', 'Third_quartile', 'Maximum'],
        orientation='h'
    )]
    layout = go.Layout(
        width=360,
        height=195,
        margin=go.Margin(
            l=100,
            r=50,
            b=30,
            t=20,
        ),

    )
    fig21 = go.Figure(data=data, layout=layout)

    fig22 = plot(fig21, output_type='div', show_link=False)

    return fig22

#graph for value
def graph_value():

    data_1 = [go.Bar(
        x=[10000, 7500, 5000, 2000, 500],
        y=['Very High', 'High', 'Medium', 'Low', 'Very Low'],
        orientation='h'
    )]
    layout_1 = go.Layout(
        width=360,
        height=165,
        margin=go.Margin(
            l=100,
            r=50,
            b=30,
            t=20,
        ),

    )
    fig09 = go.Figure(data=data_1, layout=layout_1)

    fig23 = plot(fig09, output_type='div', show_link=False)

    return fig23

def graph_engagement():
    data = [go.Bar(
        x=[10000, 7500, 5000, 2000, 500],
        y=['Very High', 'High', 'Medium', 'Low', 'Very Low'],
        orientation='h'
    )]
    layout = go.Layout(
        width=360,
        height=165,
        margin=go.Margin(
            l=100,
            r=50,
            b=30,
            t=20,
        ),

    )
    fig = go.Figure(data=data, layout=layout)

    fig1 = plot(fig, output_type='div', show_link=False)

    return fig1

def graph_profile():
    pass