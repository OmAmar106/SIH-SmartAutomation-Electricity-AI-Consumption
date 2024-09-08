import pandas as pd
from prophet import Prophet
import plotly.express as px
import plotly.io as pio
from meteostat import Point, Daily
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
import plotly.graph_objects as go
import os

cur = os.path.dirname(os.path.realpath(__file__))
file1 =  cur+'/static/datasets/power_Generation.json'
file2 = cur+'/static/datasets/rene_energy.json'

def stats(year):
    Power_Generation = pd.read_json(file1)
    Power_Generation['fy'] = pd.to_datetime(Power_Generation['fy'].str[:4], format='%Y')
    Power_Generation['Month'] = pd.to_datetime(Power_Generation['Month'], format='%b-%Y')
    Power_Generation['Month'] = Power_Generation['Month'].dt.month
    Power_y = Power_Generation.loc[Power_Generation['fy'].dt.year == year]
    share_df = Power_y.groupby(['mode'])['bus'].sum().reset_index()
    fig = px.pie(share_df, values='bus', names='mode', title='Contribution from each source in the year '+str(year))
    thermal_val = share_df.loc[share_df['mode'] == 'THERMAL', 'bus'].values[0] if not share_df.loc[share_df['mode'] == 'THERMAL', 'bus'].empty else 0
    nuclear_val = share_df.loc[share_df['mode'] == 'NUCLEAR', 'bus'].values[0] if not share_df.loc[share_df['mode'] == 'NUCLEAR', 'bus'].empty else 0
    hydro_val = share_df.loc[share_df['mode'] == 'HYDRO', 'bus'].values[0] if not share_df.loc[share_df['mode'] == 'HYDRO', 'bus'].empty else 0

    cat = ['Thermal', 'Nuclear', 'Hydro']
    values = [thermal_val, nuclear_val, hydro_val]

    fig1 = go.Figure([go.Bar(x=cat, y=values)])
    fig1.update_layout(
        title="Production in Different Sectors in the year "+str(year),
        xaxis_title="Modes",
        yaxis_title="Power (GW)"
    )
    return pio.to_json(fig),pio.to_json(fig1)
    #historical dikha raha hain 
    #val - 2019-24 dono figure dikhado 
    #fig - pie chart hain  , fig1 - bar graph 

def thermal(year):
    Power_Generation = pd.read_json(file1)
    Power_Generation['fy'] = pd.to_datetime(Power_Generation['fy'].str[:4], format='%Y')
    Power_Generation['Month'] = pd.to_datetime(Power_Generation['Month'], format='%b-%Y')
    print(Power_Generation.columns)
    thermal_df = Power_Generation[Power_Generation['mode']=='THERMAL']
    thermal_df.rename(columns={'Month':'ds','bus':'y'},inplace=True)
    husn = Prophet()
    husn.fit(thermal_df[['ds','y']])
    future = husn.make_future_dataframe(periods=year, freq='MS')
    forecast = husn.predict(future)
    fig = px.line(forecast, x='ds', y='yhat', title='Thermal Production')
    fig.update_layout(
        xaxis_title='Time',
        yaxis_title='Power(GW)',
        autosize=True
    )
    return pio.to_json(fig)
    #1-12 dono main bhai
    #forecast kar raha hain upar wala 

def renewable(year):
    ren_df = pd.read_json(file2)
    ren_df['Month'] = pd.to_datetime(ren_df['Month'], format='%b-%Y')
    ren_df = ren_df[ren_df['State']=='Delhi']
    fil_df = ren_df.iloc[1:]
    delhi_df = fil_df[['Month','total']]
    delhi_df = delhi_df.drop(1170)
    delhi_df.rename(columns={'Month':'ds','total':'y'},inplace=True)
    Gul = Prophet()
    Gul.fit(delhi_df[['ds','y']])
    future = Gul.make_future_dataframe(periods=year,freq='MS')
    forecast = Gul.predict(future)
    fig = px.line(forecast,x='ds',y='yhat',title='Renewable Energy Production')
    fig.update_layout(
        xaxis_title='Time',
        yaxis_title='Power(GW)',
        autosize = True
    )
    return pio.to_json(fig)
    #fprecasting model hain 
