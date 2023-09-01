import plotly.io as pio
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, callback, Output, Input
#from dash_iconify import DashIconify
import plotly.express as px
import pandas as pd

pio.templates.default = "seaborn"

# Use the tips data set
df = px.data.tips()

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = dbc.Container(
    [
        html.H1('Tips Dashboard', style={'textAlign':'center'}),
        html.Hr(),
        
        dbc.Row(
        [
            dbc.Col(dcc.Dropdown(df.day.unique(), 'Sun', id='dropdown-selection'), width=4),
            dbc.Col(dcc.Markdown(id='total-label'), width=4),
        ], justify='center',
        ),
        dbc.Row(
        [
            dcc.Graph(id='scatter-graph'),
        ]
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="pie-graph"), width=4),
                dbc.Col(dcc.Graph(id="box-graph"), width=8),
            ],
            align="center",
        ),
    ],
    fluid=False 
)


@callback(
    [
        Output('scatter-graph', 'figure'),
        Output('pie-graph', 'figure'),
        Output('box-graph', 'figure'),
        Output('total-label', 'children')
    ],
    Input('dropdown-selection', 'value')
)
def update_graphs(value):
    dff = df[df.day==value]
    
    scatt = px.scatter(dff, x='total_bill', y='tip', color='smoker')
    pie = px.pie(dff, values='tip', names='smoker')
    box = px.box(dff, x="time", y="total_bill", color="smoker")
    text = f'** #{dff.shape[0]} rows **'
    return scatt, pie, box, text


if __name__ == '__main__':
    app.run(debug=True)
