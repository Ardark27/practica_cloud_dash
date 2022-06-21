from click import option
import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import utils as ut
from dash.dependencies import Input, Output
import db 

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,
external_stylesheets=external_stylesheets)
server = app.server


dates_list = db.get_all_dates()
a = db.get_data_from_date(dates_list[0])
option_type = ['CALL', 'PUT']

app.layout = html.Div([
    html.Div([
            html.H2("Options Dashboard"),
            html.Br(),
            html.H6("Type of option: "),
            dcc.RadioItems(
                id='option-type',
                options=[{'label': i, 'value': i} for i in option_type],
                value='CALL',
                inline= True
            ),
            html.H6("Day of data extraction: "),
            dcc.Dropdown(
                id='data-date'
            ),
            html.H6("Date: "),
            dcc.Dropdown(
                id='option-date'
            ),
            html.H6("Data Avaliable"),
            dcc.RadioItems(
                id='option-data-available',
                options=[{'label': i, 'value': i} for i in ['prices', 'impliedVolatility']],
                value='impliedVolatility',
                inline= True
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),
    dcc.Graph(
        id='display-selected-values'
    )
])

@app.callback(
    Output('data-date', 'options'),
    Input('date-search', 'value'))
def set_date_data(date_search):
    for i in a.keys():
        for j in a[i].keys():
            if j == option_type:
                return [{'label': i, 'value': i} for i in a[i][j].keys()]

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
    Input('option-type', 'value'),
    Input('option-data-available', 'value'))
def set_display_children(option_date, option_type, option_data_availiable):
    for i in a.keys():
        strike = a[i][option_type][option_date]['strikes']
        data = a[i][option_type][option_date][option_data_availiable]
    
    df = pd.DataFrame({'Strike': strike, option_data_availiable : data})
    fig = px.line(df, x='Strike', y=f'{option_data_availiable}', markers = True)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0", port=8080, use_reloader=True)