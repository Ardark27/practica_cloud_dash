from click import option
import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import utils as ut
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,
external_stylesheets=external_stylesheets)

a = ut.load_json('14_06_2022.json')
option_type = ['CALL', 'PUT']

app.layout = html.Div([
    html.Div([
            html.H2("Options Dashboard"),
            html.Br(),
            html.H6("Type of option: "),
            dcc.Dropdown(
                id='option-type',
                options=[{'label': i, 'value': i} for i in option_type],
                value='CALL'
            ),
            html.H6("Date: "),
            dcc.Dropdown(
                id='option-date'
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),
    dcc.Graph(
        id='display-selected-values'
    )
])

@app.callback(
    Output('option-date', 'options'),
    Input('option-type', 'value'))
def set_tickers(option_type):
    for i in a.keys():
        for j in a[i].keys():
            if j == option_type:
                return [{'label': i, 'value': i} for i in a[i][j].keys()]



@app.callback(
    Output('option-date', 'value'),
    Input('option-date', 'options'))
def set_cities_value(option_date):
    return option_date[0]['value']


@app.callback(
    Output('display-selected-values', 'figure'),
    Input('option-date', 'value'),
    Input('option-type', 'value'))
def set_display_children(option_date, option_type):
    for i in a.keys():
        strike = a[i][option_type][option_date]['strikes']
        volatility = a[i][option_type][option_date]['impliedVolatility']
    
    df = pd.DataFrame({'Strike': strike, 'Implied Volatility': volatility})
    fig = px.line(df, x='Strike', y='Implied Volatility')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)