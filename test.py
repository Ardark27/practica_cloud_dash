
import src.utils as ut
import pandas as pd
import plotly.graph_objects as go

a = ut.load_json('src/14_06_2022.json')

def main(day_to_compare = '14-06-2022'):
    call = pd.DataFrame()
    put = pd.DataFrame()
    for i in a.keys():  # i fecha de adquisicion
        for j in a[i].keys():  # j tipo de opcion/futuro
            if j != 'FUTURO':
                for k in a[i][j].keys():  # dates de opciones
                    strikes = a[i][j][k]['strikes']
                    impliedVolatility = a[i][j][k]['impliedVolatility']
                    delta_days =(pd.to_datetime(k) - pd.to_datetime(day_to_compare)).days
                    if delta_days == 0:
                        delta_days = 0.5 
                    if j == 'CALL':
                        call_1 = pd.DataFrame(data = [impliedVolatility], columns=strikes, index=[delta_days])
                        call = pd.concat([call, call_1])
                    elif j == 'PUT':
                        put_1 = pd.DataFrame(data = [impliedVolatility], columns=strikes, index=[delta_days])
                        put = pd.concat([put, put_1])
    return call, put

def pintame(data):
    z=data.values
    x=data.columns
    y=data.index
    fig = go.Figure(data=[go.Surface(z=z, x=x, y=y)])
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



if __name__ == '__main__':
    call, put  = main()
    pintame(call)