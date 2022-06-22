from click import option
import dash
from dash import dcc
from dash import html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import utils as ut
from dash.dependencies import Input, Output
import db 

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,
external_stylesheets=external_stylesheets)
server = app.server


dates_list = db.get_all_dates()

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
            html.H6("Date of data extraction: "),
            dcc.Dropdown(
                id='data-date',
                options=[{'label': i, 'value': i} for i in dates_list],
                value = dates_list[0]
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
    ),
    dcc.Graph(
        id='display-surface'
    ),
    dcc.Slider(0,len(dates_list)-1,step=None,
        id='slider-surface',
        marks={i:dates_list[i] for i in range(len(dates_list))},
        value=0
    ),
    html.Br(),
    # dcc.Dropdown(
    #     id='option-date-compare-one',
    #     options=[{'label': i, 'value': i} for i in dates_list],
    #     value = dates_list[0]
    # ),
    # dcc.Dropdown(
    #     id='option-date-compare-two',
    #     options=[{'label': i, 'value': i} for i in dates_list],
    #     value = dates_list[1]
    # ),
    # dcc.Graph(
    #     id='display-compare-days'
    # ),
])



@app.callback(
    Output('option-date', 'options'),
    Input('option-type', 'value'),
    Input('data-date', 'value'))
def set_tickers(option_type,data_date):
    global a
    a = db.get_data_from_date(data_date)
    for j in a.keys():
        if j == option_type:
            return [{'label': i, 'value': i} for i in a[j].keys()]



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

    strike = a[option_type][option_date]['strikes']
    data = a[option_type][option_date][option_data_availiable]
    
    df = pd.DataFrame({'Strike': strike, option_data_availiable : data})
    fig = px.line(df, x='Strike', y=f'{option_data_availiable}', markers = True)
    return fig

# @app.callback(
#     Output('display-compare-days', 'figure'),
#     Input('option-date', 'value'),
#     Input('option-date-compare-one', 'value'),
#     Input('option-date-compare-two', 'value'),
#     Input('option-type', 'value'),
#     Input('option-data-available', 'value'))
# def set_display_compare_days(option_date,option_date_compare_one,option_date_compare_two,option_type, option_data_availiable):
    
#     b = db.get_data_from_date(option_date_compare_two)
#     c = db.get_data_from_date(option_date_compare_one)
#     print(b['CALL'].keys())
#     strike = c[option_type][option_date]['strikes']
#     data = c[option_type][option_date][option_data_availiable]
    
#     strike_day2 = b[option_type][option_date]['strikes']
#     data_day2 = b[option_type][option_date][option_data_availiable]
    
#     df = pd.DataFrame({'Strike': strike, option_data_availiable : data})
#     df_day2 = pd.DataFrame({'Strike': strike_day2, option_data_availiable : data_day2})
#     fig = px.line(df, x='Strike', y=f'{option_data_availiable}', markers = True)
#     fig = px.line(df_day2, x='Strike', y=f'{option_data_availiable}', markers = True)
#     return fig

@app.callback(
    Output('display-surface', 'figure'),
    Input('option-type', 'value'),
    Input('slider-surface', 'value'))
def set_display_surface_children(option_type,data_date):
    
    a = db.get_data_from_date(dates_list[data_date])

    option_data = ut.data_to_df(dates_list[data_date],a,option_type)
    X,Y,Z = ut.prepare_df_to_graph(option_data)

    fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y)])
    fig.update_layout(title='Superficie de volatidad', autosize=False,
                    width=500, height=500,
                    margin=dict(l=65, r=50, b=65, t=90),
                    scene=dict(
                        xaxis_title='Strike',
                        yaxis_title='Days_to_go',
                        zaxis_title='ImpliedVolatility'
                    ))

    return fig


if __name__ == '__main__':
    app.run_server(debug=False, host="0.0.0.0", port=8080, use_reloader=True)