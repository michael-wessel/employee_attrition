from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from utilities import utilities, donuts, table

# Initialize the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    [
        # Top Row
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1('Work Sample Challenge'),
                        html.H2('Developed by: Michael Wessel'),
                        html.Hr()
                    ]
                )
            ]
        ), 

        # Question Row
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H3('Research Question:'),
                        html.P('Using the sample data provided, are women leaving at a significantly higher or lower rate than men?'),
                    ]
                )
            ]
        ), 

        # Second Row
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            className='div-for-table',                                                       
                            children=[
                                table.generate_table(table.data)
                            ], 
                            style={
                                'display': 'inline-block', 
                                'margin': '0px 0px 10px 10px'
                            }
                        ),
                        dbc.Row(
                            html.H4('Select a Departure Type:', style={'height': '10%','margin': '0px 0px 5px 15px'}),
                        ),                        
                        dbc.Row(
                            [
                                dbc.FormGroup(
                                    [
                                        dbc.RadioItems(
                                            options=[
                                                {'label': 'All Departures', 'value': 'Total Rate'},
                                                {'label': 'Layoffs', 'value': 'Layoff Rate'},
                                                {'label': 'Resignation', 'value': 'Resignation Rate'},
                                                {'label': 'Retirement', 'value': 'Retirement Rate'},
                                                {'label': 'Voluntary', 'value': 'Voluntary Rate'},
                                            ],
                                            value='Total Rate',
                                            id='departure-input',
                                            inline=True
                                        ),
                                    ]
                                )
                            ],
                            style={'margin': '0px 0px 0px 0px'}
                        )
                    ],
                    width=7
                ),
                dbc.Col(
                    [
                        dbc.Row(
                            html.H4('Departures and Types by Gender:', style={'height': '10%'}),
                        ),
                        dbc.Row(
                            [
                                dcc.Graph(figure=donuts.males, style={'display': 'inline-block', 'width': '50%'}),
                                dcc.Graph(figure=donuts.females, style={'display': 'inline-block', 'width': '50%'})
                            ],
                            style={'height': '90%'}
                        ), 
                    ],
                    width=5
                )
            ],
            style={'height': '30%'}
        ),
        # Bottom Row
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Row(
                                            html.H4('Chart Type:', style={'height': '10%', 'margin': '0px 0px 0px 15px'}),
                                        ), 
                                        dbc.Row(
                                            [
                                                dbc.FormGroup(
                                                    [
                                                        dbc.RadioItems(
                                                            options=[
                                                                {'label': 'Line', 'value': 'Line'},
                                                                {'label': 'Bar', 'value': 'Bar'}
                                                            ],
                                                            value='Line',
                                                            id='type-input',
                                                            inline=True
                                                        ),
                                                    ],
                                                    style={'margin': '5px 0px 0px 15px'}
                                                ),
                                            ]
                                        )
                                    ], width=2
                                ),
                                dbc.Col(
                                    [
                                        dbc.Row(
                                            html.H4('Annual Rates by Gender:', style={'height': '10%', 'margin': '0px 0px 0px 15px'}),
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.FormGroup(
                                                    [
                                                        dbc.RadioItems(
                                                            options=[
                                                                {'label': 'Females', 'value': 'Female'},
                                                                {'label': 'Males', 'value': 'Male'}
                                                            ],
                                                            value='Female',
                                                            id='gender2-input',
                                                            inline=True,
                                                        ),
                                                    ],
                                                    style={'margin': '5px 0px 0px 15px'}
                                                ),
                                            ]
                                        )
                                    ], width=3
                                )
                            ], style={'height': '10%'}
                        ), 
                        dbc.Row(
                            [
                                dcc.Graph(id='line', style={'width': '100%'})
                            ], style={'height': '40%'}
                        )
                    ],
                    width=12
                )
            ],
        style={'height': '90%'}
        )
    ],
    style={
    'height': '100vh'
    }
)

@app.callback(
    Output('line', 'figure'),
    Input('departure-input', 'value'),
    Input('gender2-input', 'value'),
    Input('type-input', 'value'))
def update_line(radio_value, gender2_value, type_value):
    reason = radio_value
    gender = gender2_value
    chart_type = type_value

    if chart_type == 'Bar':
        df = utilities.df
        regression_df = df.loc[df['gender_full'] == gender]
        regression_df = regression_df.groupby(by=['STATUS_YEAR', 'termreason_desc'])['EmployeeID'].nunique()
        regression_df = regression_df.unstack('termreason_desc')
        regression_df = regression_df.fillna(0)
        regression_df.rename(columns = {'Resignaton':'Resignation'}, inplace = True)
        regression_df['Total Departures'] = regression_df['Layoff'] + regression_df['Resignation'] + regression_df['Retirement']
        regression_df['Gender'] = gender
        regression_df = regression_df.reset_index()
        a_m = (regression_df['Not Applicable'].rolling(min_periods=1, window=2).sum())/2
        b_m = df[(df['STATUS_YEAR'] == 2006) & (df['orighiredate_key'] <= '2005-12-31') & (df['gender_full'] == gender)].nunique()
        c_m = regression_df.at[0,'Not Applicable']
        d_m = (b_m['EmployeeID'] + c_m) / 2
        regression_df.loc[regression_df['STATUS_YEAR'] != 2006, 'Average Number of Employees'] = a_m
        regression_df.loc[regression_df['STATUS_YEAR'] == 2006, 'Average Number of Employees'] = d_m
        regression_df['Total Rate'] = (regression_df['Total Departures'] / regression_df['Average Number of Employees'])
        regression_df['Resignation Rate'] = (regression_df['Resignation'] / regression_df['Average Number of Employees'])
        regression_df['Retirement Rate'] = (regression_df['Retirement'] / regression_df['Average Number of Employees'])
        regression_df['Layoff Rate'] = (regression_df['Layoff'] / regression_df['Average Number of Employees'])
        regression_df['Voluntary Rate'] = ((regression_df['Resignation'] + regression_df['Retirement']) / regression_df['Average Number of Employees'])

        if radio_value == 'Total Rate':
            y = regression_df['Total Rate']
        elif radio_value == 'Layoff Rate':
            y = regression_df['Layoff Rate']
        elif radio_value == 'Resignation Rate':
            y = regression_df['Resignation Rate']
        elif radio_value == 'Retirement Rate':
            y = regression_df['Retirement Rate']
        elif radio_value == 'Voluntary Rate':
            y = regression_df['Voluntary Rate']
        
        Y=y
        X=regression_df['STATUS_YEAR']

        # regression
        reg = LinearRegression().fit(np.vstack(X), Y)
        regression_df['bestfit'] = reg.predict(np.vstack(X))

        # Bar Chart with regression
        fig=go.Figure()
        fig.add_trace(go.Bar(name=gender, x=X, y=Y.values))
        fig.add_trace(go.Scatter(name='Regression Line', x=X, y=regression_df['bestfit'], mode='lines'))

        # plotly figure layout
        fig.update_layout(xaxis_title = 'Departure Rate', yaxis_title = 'Year')

        fig.update_layout(
            margin=dict(
                l=75,
                r=0,
                b=0,
                t=0
            ),
            plot_bgcolor='white',
            hovermode='x',
            xaxis=dict(
                tickmode='linear'
            ),    
        )
        fig.update_xaxes(showline=True, linewidth=1, linecolor='black')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
        fig.update_yaxes(showline=True, linewidth=1, linecolor='black')
        fig.update_xaxes(title_text='Year')
        fig.update_yaxes(title_text='Departure Rate')
        return fig

    else:
        fig = px.line(
            utilities.plot_df, 
            x='STATUS_YEAR', 
            y=reason,
            color='Gender'
        )

        fig.update_traces(
            mode='markers+lines', 
            hovertemplate=None
        )

        fig.update_layout(
            margin=dict(
                l=75,
                r=0,
                b=0,
                t=10
            ),
            plot_bgcolor='white',
            legend_title_text='Gender',
            hovermode='x unified',
            xaxis=dict(
                tickmode='linear'
            ),    
            yaxis=dict(
                ticksuffix='%',
            )
        )

        fig.update_xaxes(showline=True, linewidth=1, linecolor='black')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
        fig.update_yaxes(showline=True, linewidth=1, linecolor='black')
        fig.update_xaxes(title_text='Year')
        fig.update_yaxes(title_text='Departure Rate')
        return fig

if __name__ == '__main__':
    app.run_server(port=8050, debug=True)