import pandas as pd
from prophet import Prophet
import plotly.express as px
from meteostat import Point, Daily
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
import os
import platform
import plotly.io as plo
import plotly.express as px
from plotly.io import to_image

cur = os.path.dirname(os.path.realpath(__file__))
delhi_file_path =  cur+'/static/datasets/delhi.csv'
delhi_peak_file_path = cur+'/static/datasets/delhi_peak.csv'
def model1(val):
    delhi = pd.read_csv(delhi_file_path)
    delhi['Month'] = pd.to_datetime(delhi['Month'])
    delhi.sort_values('Month', inplace=True)
    holidays = pd.DataFrame({
        'holiday': ['Anomaly'],
        'ds': ['2022-06-01']
    })
    holidays['ds'] = pd.to_datetime(holidays['ds'])
    delhi.rename(columns={'Month': 'ds', 'energy_requirement': 'y', 'tmax': 'tavg'}, inplace=True)
    delhi['ds'] = pd.to_datetime(delhi['ds'])
    model = Prophet(holidays=holidays)
    model.add_regressor('tavg')
    model.fit(delhi[['ds', 'y', 'tavg']])
    future = model.make_future_dataframe(periods=val, freq='MS')
    delhi_location = Point(28.6139, 77.2090)
    current_date = datetime.now()
    start_date = datetime(current_date.year, current_date.month, 1) + relativedelta(months=1)
    end_date = start_date + relativedelta(months=val)
    weather_data = Daily(delhi_location, start=start_date, end=end_date)
    weather_data = weather_data.fetch()
    weather_data.reset_index(inplace=True)
    future = future.merge(weather_data[['time', 'tavg']], left_on='ds', right_on='time', how='left')
    future.drop(columns=['time'], inplace=True)
    future['tavg'] = future['tavg'].fillna(delhi['tavg'].mean())
    forecast = model.predict(future)
    fig = px.line(forecast, x='ds', y='yhat', title='Forecasted Energy Requirement')
    fig.update_layout(
        xaxis_title='Time',
        yaxis_title='Power in MWH',
        autosize=True
    )
    return forecast, fig

def model2(val):
    delhi = pd.read_csv(delhi_peak_file_path)
    delhi['Month'] = pd.to_datetime(delhi['Month'])
    delhi.sort_values('Month', inplace=True)
    holidays = pd.DataFrame({
        'holiday': ['Anomaly'],
        'ds': ['2022-06-01']
    })
    holidays['ds'] = pd.to_datetime(holidays['ds'])
    delhi.rename(columns={'Month': 'ds', 'peak_demand': 'y', 'tmax': 'tavg'}, inplace=True)
    delhi['ds'] = pd.to_datetime(delhi['ds'])
    model = Prophet(holidays=holidays)
    model.add_regressor('tavg')
    model.fit(delhi[['ds', 'y', 'tavg']])
    future = model.make_future_dataframe(periods=val, freq='MS')
    delhi_location = Point(28.6139, 77.2090)
    current_date = datetime.now()
    start_date = datetime(current_date.year, current_date.month, 1) + relativedelta(months=1)
    end_date = start_date + relativedelta(months=val)
    weather_data = Daily(delhi_location, start=start_date, end=end_date)
    weather_data = weather_data.fetch()
    weather_data.reset_index(inplace=True)
    future = future.merge(weather_data[['time', 'tavg']], left_on='ds', right_on='time', how='left')
    future.drop(columns=['time'], inplace=True)
    future['tavg'] = future['tavg'].fillna(delhi['tavg'].mean())
    forecast = model.predict(future)
    fig = px.line(forecast, x='ds', y='yhat', title='Forecasted Peak')
    fig.update_layout(
        xaxis_title='Time',
        yaxis_title='Peak Power in MWH',
        autosize=True
    )
    return forecast, fig

def model3():
    forecast1,x = model1(1)
    forecast2,x = model2(1)
    current_month_forecast = forecast1[forecast1['ds'].dt.month == datetime.now().month].iloc[0]
    current_month_peak = forecast2[forecast2['ds'].dt.month == datetime.now().month].iloc[0]
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday = today - timedelta(days=1)
    delhi_location = Point(28.6139, 77.2090)
    weather_data_today = Daily(delhi_location, start=today, end=today)
    weather_data_today = weather_data_today.fetch()
    if weather_data_today.empty:
        weather_data_yesterday = Daily(delhi_location, start=yesterday, end=yesterday)
        weather_data_yesterday = weather_data_yesterday.fetch()
        if not weather_data_yesterday.empty:
            avg_temp_today = weather_data_yesterday['tavg'].mean()
        else:
            avg_temp_today = 'Data not available'
    else:
        avg_temp_today = weather_data_today['tavg'].mean()
    return [current_month_peak,current_month_forecast,avg_temp_today]


def model4(val):
    _, img1 = model1(val)
    _, img2 = model2(val)
    img1.write_image(cur+'/static/images/'+str(val)+'file1.png',format='png',engine='kaleido')
    img2.write_image(cur+'/static/images/'+str(val)+'file2.png',format='png',engine='kaleido')
# forecast1, fig1 = model1(5)
# forecast2, fig2 = model2(5)

# # Save figures as images
# pio.show(fig1)
# pio.show(fig2)

# # Display the forecast and temperature metrics
# current_month_forecast = forecast1[forecast1['ds'].dt.month == datetime.now().month].iloc[0]
# current_month_peak = forecast2[forecast2['ds'].dt.month == datetime.now().month].iloc[0]



# print(current_month_forecast,current_month_peak)

# Create columns for side-by-side plotting with full width


# col1, col2 = st.columns([1, 1])

# with col1:
#     forecast1, fig1 = model1(val)
#     st.plotly_chart(fig1, use_container_width=True)

# with col2:
#     forecast2, fig2 = model2(val)
#     st.plotly_chart(fig2, use_container_width=True)

# # # Display the forecast and temperature metrics
# # st.write("### Current Metrics")

# # # Get the forecast for the current month
# forecast1,x = model1(1)
# forecast2,x = model2(1)
# current_month_forecast = forecast1[forecast1['ds'].dt.month == datetime.now().month].iloc[0]
# current_month_peak = forecast2[forecast2['ds'].dt.month == datetime.now().month].iloc[0]

# # Create columns for metrics
# metric_col1, metric_col2, metric_col3 = st.columns(3)

# with metric_col1:
#     st.metric(label="This Month's Peak", value=f"{current_month_peak['yhat']:.2f} MWH")

# with metric_col2:
#     st.metric(label="This Month's Avg Energy Requirement", value=f"{current_month_forecast['yhat']:.2f} MWH")

# today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
# yesterday = today - timedelta(days=1)
# delhi_location = Point(28.6139, 77.2090)
# weather_data_today = Daily(delhi_location, start=today, end=today)
# weather_data_today = weather_data_today.fetch()
#current month forecast - average usage of current month 
#current monrth peak - peak voltage of current mornth 
#put todays date 

# if weather_data_today.empty:
#     weather_data_yesterday = Daily(delhi_location, start=yesterday, end=yesterday)
#     weather_data_yesterday = weather_data_yesterday.fetch()
#     if not weather_data_yesterday.empty:
#         avg_temp_today = weather_data_yesterday['tavg'].mean()
#     else:
#         avg_temp_today = 'Data not available'
#avg_temp_today gets average temperature kya hain 


# else:
#     avg_temp_today = weather_data_today['tavg'].mean()

# with metric_col3:
#     st.metric(label="Today's Avg Temperature", value=f"{avg_temp_today:.2f} °C" if avg_temp_today != 'Data not available' else avg_temp_today)

