import time

import dash
import dash_bootstrap_components as dbc
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
from dash import Input, Output, dcc, html
import db
import utils as ut

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

dates_list = db.get_all_dates()

option_type = ['CALL', 'PUT']

app.layout = dbc.Container(
    [
        dcc.Store(id="store"),
        html.H1("Options Dashboard"),
        html.Hr(),
        dbc.Tabs(
            [
                dbc.Tab(label="Opción simple", tab_id="option-simple"),
                dbc.Tab(label="Comparación de opciones", tab_id="option-comparator"),
                dbc.Tab(label="Superficie de volatilidad", tab_id="surface-vol"),
            ],
            id="tabs",
            active_tab="option-simple",
        ),
        html.Div(
            id="tab-content",
            className="p-4",
            ),

    ]
)


@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab")],
)
def render_tab_content(active_tab):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """
    if active_tab is not None:
        # we have the entire option-simple tab here
        if active_tab == "option-simple":
            content = [
                html.H6("Type of option: "),
            dbc.RadioItems(
                id='option-type',
                className="btn-group",
                inputClassName="btn-check",
                labelClassName="btn btn-outline-primary",
                labelCheckedClassName="active",
                options=[{'label': i, 'value': i} for i in option_type],
                value='CALL'
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
            dbc.RadioItems(
                id='option-data-available',
                className="btn-group",
                inputClassName="btn-check",
                labelClassName="btn btn-outline-primary",
                labelCheckedClassName="active",
                options=[{'label': i, 'value': i} for i in ['prices', 'impliedVolatility']],
                value='impliedVolatility'
            ),
            dcc.Graph(
                id='display-option-simple'
            )
            ]
            return content
        elif active_tab == "option-comparator":
            content=['Aqui hay que poner todo la pagina de las comparaciones']
            return content
        elif active_tab == "surface-vol":
            content = [
                dbc.RadioItems(
                    id='option-type',
                    className="btn-group",
                    inputClassName="btn-check",
                    labelClassName="btn btn-outline-primary",
                    labelCheckedClassName="active",
                    options=[{'label': i, 'value': i} for i in option_type],
                    value='CALL'
                ),
                dcc.Graph(
                        id='display-surface'
                ),
                dcc.Slider(0,len(dates_list)-1,step=None,
                    id='slider-surface',
                    marks={i:dates_list[i] for i in range(len(dates_list))},
                    value=0
                )
            ]
            return content
    return "No tab selected"

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
    Output('display-option-simple', 'figure'),
    Input('option-date', 'value'),
    Input('option-type', 'value'),
    Input('option-data-available', 'value'))
def set_display_children(option_date, option_type, option_data_availiable):

    strike = a[option_type][option_date]['strikes']
    data = a[option_type][option_date][option_data_availiable]
    
    df = pd.DataFrame({'Strike': strike, option_data_availiable : data})
    fig = px.line(df, x='Strike', y=f'{option_data_availiable}', markers = True)
    return fig

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



if __name__ == "__main__":
    app.run_server(debug=False, port=8888)