import pandas as pd
import plotly.graph_objects as go 
from utilities import utilities

df = utilities.df
data = df.copy()

female_plot = data.loc[(data['gender_full'] == 'Female') & (data['STATUS'] != 'ACTIVE')]
female_plot = female_plot.groupby(female_plot['termreason_desc'])['EmployeeID'].nunique()
female_plot = female_plot.reset_index()
female_label = data.loc[(data['gender_full'] == 'Female') & (data['STATUS'] != 'ACTIVE')]
female_label = female_label.groupby(female_label['termreason_desc'])['EmployeeID'].nunique()
female_label = female_label.sum().astype(str)

male_plot = data.loc[(data['gender_full'] == 'Male') & (data['STATUS'] != 'ACTIVE')]
male_plot = male_plot.groupby(male_plot['termreason_desc'])['EmployeeID'].nunique()
male_plot = male_plot.reset_index()
male_label = data.loc[(data['gender_full'] == 'Male') & (data['STATUS'] != 'ACTIVE')]
male_label = male_label.groupby(male_label['termreason_desc'])['EmployeeID'].nunique()
male_label = male_label.sum().astype(str)

males = go.Figure(
    layout=go.Layout(
        margin={'t': 25, 'b': 35, 'l': 25, 'r': 25},
        showlegend=False, 
        annotations=[
            dict(
                text=male_label,
                x=0.5,
                y=0.55,
                font=dict(
                    size=40,
                ),
                showarrow=False),
            dict(
                text='MALES',
                x=0.5,
                y=0.4,
                font_size=14,
                showarrow=False
            )
        ]
    )
)
males.add_trace(
    go.Pie(
        labels=male_plot['termreason_desc'],
        values=male_plot['EmployeeID'],
        textinfo='none'
    )
)
males.update_traces(
    hole=.8,
    hoverinfo='percent+value+label',
)
males.update_xaxes(automargin=True)
males.update_yaxes(automargin=True)

# Female Donut
females = go.Figure(
    layout=go.Layout(
        margin={'t': 25, 'b': 35, 'l': 25, 'r': 25},
        showlegend=False, 
        annotations=[
            dict(
                text=female_label,
                x=0.5,
                y=0.55,
                font=dict(
                    size=40,
                ),
                showarrow=False),
            dict(
                text='FEMALES',
                x=0.5,
                y=0.4,
                font_size=14,
                showarrow=False
            )
        ]
    )
)
females.add_trace(
    go.Pie(
        labels=female_plot['termreason_desc'],
        values=female_plot['EmployeeID'],
        textinfo='none'
    )
)
females.update_traces(
    hole=.8,
    hoverinfo='percent+value+label',
)
females.update_xaxes(automargin=True)
females.update_yaxes(automargin=True)