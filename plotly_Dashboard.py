import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import csv



#dashboard stuff
df = pd.read_csv('data.csv')
df_rank = pd.read_csv("rank.csv")
          


#Read CSV and plot the chart
fig = make_subplots(
    rows=8, cols=3,
    specs=[[{}, {"rowspan": 2,"colspan": 2},None],
        [{}, None,None],
        [{}, None,None],
        [{}, None,None],
        [{}, None,None],
        [{}, None,None],
        [{}, None,None],
        [{}, None,None]],
    subplot_titles=("Sanjay","Rank tracking", "Thamar", "Abhishek", "Shishir","Nivin","Diraj","Nithin","Hrideek"))
fig.add_trace(
    go.Scatter(
    x=df['Game No'], 
    y=df['Sanjay'], name="Sanjay",line_shape='spline',connectgaps=True,showlegend=False),
    row=1, col=1
)

fig.add_trace(
    go.Scatter(
    x=df['Game No'], 
    y=df['thamarmo'], name="Thamar",line_shape='spline',connectgaps=True,showlegend=False),
    row=2, col=1
)

fig.add_trace(
    go.Scatter(
    x=df['Game No'], 
    y=df['Abhishek'], name="Abhishek",line_shape='spline',connectgaps=True,showlegend=False),
    row=3, col=1
)

fig.add_trace(
    go.Scatter(
    x=df['Game No'], 
    y=df['Shishtaouk'], name="Shishir",line_shape='spline',connectgaps=True,showlegend=False),
    row=4, col=1
)

fig.add_trace(
    go.Scatter(
    x=df['Game No'], 
    y=df['NipPincher'], name="Nivin",line_shape='spline',connectgaps=True,showlegend=False),
    row=5, col=1
)

fig.add_trace(
    go.Scatter(
    x=df['Game No'], 
    y=df['Diraj'], name="Diraj",line_shape='spline',connectgaps=True,showlegend=False),
    row=6, col=1
)

fig.add_trace(
    go.Scatter(
    x=df['Game No'], 
    y=df['SugaDaddy'], name="Nithin",line_shape='spline',connectgaps=True,showlegend=False),
    row=7, col=1
)

fig.add_trace(
    go.Scatter(
    x=df['Game No'], 
    y=df['Spartan'], name="Hrideek",line_shape='spline',connectgaps=True,showlegend=False),
    row=8, col=1
)

#Rank tracking
fig.add_trace(
    go.Scatter(
    x=df_rank['Game No'], 
    y=df_rank['Sanjay'], name='Sanjay',line_shape='spline',connectgaps=True),
    row=1,col=2
)
fig.add_trace(
    go.Scatter(
    x=df_rank['Game No'], 
    y=df_rank['thamarmo'], name = 'Thamar',line_shape='spline',connectgaps=True),
    row=1,col=2
)
fig.add_trace(
    go.Scatter(
    x=df_rank['Game No'], 
    y=df_rank['Abhishek'], name='Abhishek',line_shape='spline',connectgaps=True),
    row=1,col=2
)
fig.add_trace(
    go.Scatter(
    x=df_rank['Game No'], 
    y=df_rank['Shishtaouk'], name='Shishir',line_shape='spline',connectgaps=True),
    row=1,col=2
)
fig.add_trace(
    go.Scatter(
    x=df_rank['Game No'], 
    y=df_rank['NipPincher'], name = 'Nivin',line_shape='spline',connectgaps=True),
    row=1,col=2
)

fig.add_trace(
    go.Scatter(
    x=df_rank['Game No'], 
    y=df_rank['Diraj'], name = 'Diraj',line_shape='spline',connectgaps=True),
    row=1,col=2
)

fig.add_trace(
    go.Scatter(
    x=df_rank['Game No'], 
    y=df_rank['SugaDaddy'], name = 'Nithin',line_shape='spline',connectgaps=True),
    row=1,col=2
)

fig.add_trace(
    go.Scatter(
    x=df_rank['Game No'], 
    y=df_rank['Spartan'], name='Hrideek',line_shape='spline',connectgaps=True),
    row=1,col=2
)


fig.update_layout(height=800, width=1024, title_text="Monopoly Tracking Dashboard")
fig.show()

