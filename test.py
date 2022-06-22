
import src.utils as ut
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from scipy.interpolate import griddata
def data_to_df(day_to_compare,data,type):
    call = pd.DataFrame()
    put = pd.DataFrame()
    for j in data.keys():  # j tipo de opcion/futuro
        if j != 'FUTURO':
            for k in data[j].keys():  # dates de opciones
                strikes = data[j][k]['strikes']
                impliedVolatility = data[j][k]['impliedVolatility']
                delta_days =(pd.to_datetime(k) - pd.to_datetime(day_to_compare)).days
                if delta_days == 0:
                    delta_days = 0.5 
                if j == 'CALL':
                    call_1 = pd.DataFrame(data = [impliedVolatility], columns=strikes, index=[delta_days])
                    call = pd.concat([call, call_1])
                elif j == 'PUT':
                    put_1 = pd.DataFrame(data = [impliedVolatility], columns=strikes, index=[delta_days])
                    put = pd.concat([put, put_1])
    if type == 'CALL':
        return call
    if type == 'PUT':
        return put

def prepare_df_to_graph(option_data):
    pivot = pd.DataFrame()
    for i in option_data.index:
        for j in option_data.columns:
            data = [i,j,option_data.loc[i,j]]
            pivot_1 = pd.DataFrame(data = [data], columns=['days_to_go','strikes','imv'])
            pivot = pd.concat([pivot, pivot_1])
    pivot.dropna(inplace=True)
    x = pivot.strikes.values
    y = pivot.days_to_go.values
    z = pivot.imv.values
    xi = np.linspace(x.min(),x.max(),100)
    yi = np.linspace(y.min(),y.max(),100)
    X,Y = np.meshgrid(xi,yi)
    Z = griddata((x,y),z,(X,Y),method='cubic')
    return X, Y, Z

def pintame(X,Y,Z):
    fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y)])
    fig.update_layout(title='Superficie de volatidad', autosize=False,
                    width=500, height=500,
                    margin=dict(l=65, r=50, b=65, t=90),
                    scene=dict(
                        xaxis_title='Strike',
                        yaxis_title='Days_to_go',
                        zaxis_title='ImpliedVolatility'
                    ))
    fig.show()
    return 0



