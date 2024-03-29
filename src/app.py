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
from dash_bootstrap_templates import ThemeSwitchAIO

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP]) #[dark,light], [CYBORG,BOOTSTRAP]

template_theme1 = 'flatly'
template_theme2 = 'slate'
url_theme1 = dbc.themes.FLATLY
url_theme2 = dbc.themes.SLATE

dates_list = db.get_all_dates()
option_type = ['CALL', 'PUT']

app.layout = dbc.Container(
    [
        dcc.Store(id="store"),
        html.Br(),
        html.H1("Options Dashboard MiniIbex"),
        ThemeSwitchAIO(aio_id="theme", themes=[url_theme1, url_theme2]),
        html.Hr(),
        dbc.Tabs(
            [
                dbc.Tab(label="Opción simple", tab_id="option-simple"),
                dbc.Tab(label="Comparador de opciones", tab_id="option-comparator"),
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
    Input(ThemeSwitchAIO.ids.switch("theme"), "value"),
    [Input("tabs", "active_tab")],
)
def render_tab_content(toggle,active_tab):
    template = template_theme1 if toggle else template_theme2
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """
    if active_tab is not None:
        # we have the entire option-simple tab here
        if active_tab == "option-simple":
            content = [html.Div([
                html.H6("Tipo de opción: "),
            dbc.RadioItems(
                id='option-type',
                className="btn-group",
                inputClassName="btn-check",
                labelClassName="btn btn-outline-primary",
                labelCheckedClassName="active",
                options=[{'label': i, 'value': i} for i in option_type],
                value='CALL'
            ),
            html.H6("Fecha de toma de datos :"),
            dcc.Dropdown(
                id='data-date',
                options=[{'label': i, 'value': i} for i in dates_list],
                value = dates_list[0]
            ),
            html.H6("Día de vencimiento : "),
            dcc.Dropdown(
                id='option-date',
                
            ),
            html.H6("Datos disponibles"),
            dbc.RadioItems(
                id='option-data-available',
                className="btn-group",
                inputClassName="btn-check",
                labelClassName="btn btn-outline-primary",
                labelCheckedClassName="active",
                options=[{'label': i, 'value': j} for i,j in zip(['Precio', 'Volatilidad implícita'],['prices', 'impliedVolatility'])],
                value='impliedVolatility'
            ),
            ],
            style={'width': '45%','text-align': 'center', 'margin':'auto'}
            ),
            dcc.Graph(
                id='display-option-simple'
            )
            ]
            return content
        elif active_tab == "option-comparator":
            content=[
            html.Div([
            html.H6("Tipo de opción: "),
            dbc.RadioItems(
                id='option-type',
                className="btn-group",
                inputClassName="btn-check",
                labelClassName="btn btn-outline-primary",
                labelCheckedClassName="active",
                options=[{'label': i, 'value': i} for i in option_type],
                value='CALL'
            ),
            dbc.Row([
                html.Br(),
                dbc.Col([
                    dbc.Label("Fecha de toma de datos :"),
                    dcc.Dropdown(
                        id='first-date-compare',
                        options=[{'label': i, 'value': i} for i in dates_list],
                        value = dates_list[0],
                        clearable=False,
                    ),
                    dbc.Label("Día de vencimiento : "),
                    dcc.Dropdown(
                        id='option-date-first',
                    ),
                ]),
                html.Br(),
                dbc.Col([
                    dbc.Label("Fecha de toma de datos 2:"),
                    dcc.Dropdown(
                        id='second-date-compare',
                        options=[{'label': i, 'value': i} for i in dates_list],
                        value = dates_list[1]
                    ),
                    dbc.Label("Día de vencimiento : "),
                    dcc.Dropdown(
                        id='option-date-second',
                    ),
                ])   
            ],
            align="center",
            ),
            html.Br(),
            dcc.Graph(
                    id='display-comparator-options'
                    )
            ],
            style={'text-align': 'center', 'margin':'auto'}
            ),
            
            ]
            return content
        elif active_tab == "surface-vol":
            content = [html.Div([
                dbc.RadioItems(
                    id='option-type',
                    className="btn-group",
                    inputClassName="btn-check",
                    labelClassName="btn btn-outline-primary",
                    labelCheckedClassName="active",
                    options=[{'label': i, 'value': i} for i in option_type],
                    value='CALL'
                ),
                dcc.Slider(0,len(dates_list)-1,step=None,
                    id='slider-surface',
                    marks=None,
                    #marks={i:dates_list[i] for i in range(len(dates_list))}, # descomentar para poner fechas en el slider, pero no se ve bien
                    value=0
                ),
                html.Br(),
                html.H5(id='titulo-superficie-vol'),
                dcc.Graph(
                        id='display-surface'
                ),
                
            ],style={'width': '90%','text-align': 'center', 'margin':'auto'})]
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
    Output('option-date-first', 'options'),
    Input('option-type', 'value'),
    Input('first-date-compare', 'value'))
def set_tickers(option_type,firs_date_compare):
    global a
    a = db.get_data_from_date(firs_date_compare)
    for j in a.keys():
        if j == option_type:
            return [{'label': i, 'value': i} for i in a[j].keys()]
@app.callback(
    Output('option-date-first', 'value'),
    Input('option-date-first', 'options'))
def set_cities_value(option_date):
    return option_date[0]['value']
    
@app.callback(
    Output('option-date-second', 'options'),
    Input('option-type', 'value'),
    Input('second-date-compare', 'value'))
def set_tickers(option_type,second_date_compare):
    global a
    a = db.get_data_from_date(second_date_compare)
    for j in a.keys():
        if j == option_type:
            return [{'label': i, 'value': i} for i in a[j].keys()]
@app.callback(
    Output('option-date-second', 'value'),
    Input('option-date-second', 'options'))
def set_cities_value(option_date):
    return option_date[0]['value']


@app.callback(
    Output('option-date', 'value'),
    Input('option-date', 'options'))
def set_cities_value(option_date):
    return option_date[0]['value']

@app.callback(
    Output('titulo-superficie-vol', 'children'),
    Input('slider-surface', 'value'))
def set_title_surface(option_date):
    return f'Superficie de volatilidad día {dates_list[option_date]}'


@app.callback(
    Output('display-option-simple', 'figure'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value"),
    Input('option-date', 'value'),
    Input('option-type', 'value'),
    Input('option-data-available', 'value'))
def set_display_children(toggle,option_date, option_type, option_data_availiable):
    template = template_theme1 if toggle else template_theme2
    strike = a[option_type][option_date]['strikes']
    data = a[option_type][option_date][option_data_availiable]
    
    df = pd.DataFrame({'Strike': strike, option_data_availiable : data})
    fig = px.line(df, x='Strike', y=f'{option_data_availiable}', markers = True, template=template)
    return fig

@app.callback(
    Output('display-surface', 'figure'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value"),
    Input('option-type', 'value'),
    Input('slider-surface', 'value'))
def set_display_surface_children(toggle,option_type,data_date):
    template = template_theme1 if toggle else template_theme2
    a = db.get_data_from_date(dates_list[data_date])

    option_data = ut.data_to_df(dates_list[data_date],a,option_type)
    X,Y,Z = ut.prepare_df_to_graph(option_data)

    fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Agsunset')])
    fig.update_layout(#title='Superficie de volatidad',
                    autosize=True,
                    #width=750,
                    height=750,
                    margin=dict(l=20, r=30, b=65, t=50),
                    scene=dict(
                        xaxis_title='Strike',
                        yaxis_title='Días a vencimiento',
                        zaxis_title='Volatilidad implícita'
                    ),template=template)

    return fig


@app.callback(
    Output('display-comparator-options', 'figure'),
    Input('option-date-first', 'value'),
    Input('option-date-second', 'value'),
    Input('option-type', 'value'),
    Input('first-date-compare', 'value'),
    Input('second-date-compare', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value"),)
def set_display_comparator_children(
    option_date_first,
    option_date_second,
    option_type,
    first_date_compare,
    second_date_compare,
    toggle
    ):
    template = template_theme1 if toggle else template_theme2
    
    b = db.get_data_from_date(first_date_compare)
    c = db.get_data_from_date(second_date_compare)

    
    first_stk = b[option_type][option_date_first]['strikes']
    first_vol = b[option_type][option_date_first]['impliedVolatility']
    second_stk = c[option_type][option_date_second]['strikes']
    second_vol = c[option_type][option_date_second]['impliedVolatility']

    df_1 = pd.DataFrame({'Volatilidad implícita': first_vol, 'Strike' : first_stk,
                         'Opciones':f'Día {first_date_compare}, vencimiento {option_date_first}'}) 
    df_2 = pd.DataFrame({'Volatilidad implícita': second_vol, 'Strike' : second_stk,
                         'Opciones':f'Día {second_date_compare}, vencimiento {option_date_second}'})
    df = pd.concat([df_1,df_2])
    fig = px.line(df, x='Strike', y='Volatilidad implícita',color='Opciones', markers = True, template=template)

    return fig



if __name__ == "__main__":
   app.run_server(debug=False, host="0.0.0.0", port=8080)