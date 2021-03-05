import dash_html_components as html
import dash_bootstrap_components as dbc
from utilities import utilities

df = utilities.table_rates
data = df.copy()

def generate_table(dataframe, max_rows=500):
    return html.Table(
        # Header
        [
            html.Tr(
                [
                    html.Th(col) for col in dataframe.columns
                ]
            ) 
        ] +
        # Body
        [
            html.Tr(
                [
                    html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
                ]
            ) for i in range(min(len(dataframe), max_rows))
        ]
    )