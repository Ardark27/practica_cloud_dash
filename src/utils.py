import json
import pandas as pd
import numpy as np
from scipy.interpolate import griddata

def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)



def data_to_df(day_to_compare,data,option_type):
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
    if option_type == 'CALL':
        return call
    if option_type == 'PUT':
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
    Z[Z<0]=0
    return X, Y, Z

def process_json_data(list_items,option,key, indice):
    print(key,indice)
    stk =json.loads(list_items[indice].get('info'))[option][key]['strikes']
    vol =json.loads(list_items[indice].get('info'))[option][key]['impliedVolatility']
    return stk, vol
