from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

# Use the tips data set
df = px.data.tips()

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Tips App', style={'textAlign':'center'}),
    dcc.Dropdown(df.day.unique(), 'Sun', id='dropdown-selection'),
    dcc.Graph(id='graph-content')
])


@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)


def update_graph(value):
    dff = df[df.day==value]
    return px.scatter(dff, x='total_bill', y='tip', color='smoker')


if __name__ == '__main__':
    app.run(debug=True)
