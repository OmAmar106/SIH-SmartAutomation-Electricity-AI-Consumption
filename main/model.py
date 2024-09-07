import streamlit as st
import pandas as pd
from prophet import Prophet
import plotly.express as px
from meteostat import Point, Daily
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta

# Set the title of the app
st.title("Delhi Energy Forecast")

# Sidebar with navigation options
sidebar = st.sidebar
sidebar.title("Navigation")
selection = sidebar.radio("Go to", ["Home", "Energy Profiling", "Predicitive Management"])

if selection == "Home":
    st.header("Welcome to the Delhi Energy Forecast App")
    st.write("This app provides insights into energy forecasting and related metrics for Delhi.")
    
    val = st.slider(label="Select the months to forecast", min_value=1, max_value=12, step=1)

    def model1(val):
        delhi = pd.read_csv("C:\\Users\\91991\\Desktop\\hackathon\\delhi.csv")
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
        delhi = pd.read_csv("C:\\Users\\91991\\Desktop\\hackathon\\delhi_peak.csv")
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

    # Create columns for side-by-side plotting with full width
    col1, col2 = st.columns([1, 1])
    
    with col1:
        forecast1, fig1 = model1(val)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        forecast2, fig2 = model2(val)
        st.plotly_chart(fig2, use_container_width=True)

    # Display the forecast and temperature metrics
    st.write("### Current Metrics")

    # Get the forecast for the current month
    current_month_forecast = forecast1[forecast1['ds'].dt.month == datetime.now().month].iloc[0]
    current_month_peak = forecast2[forecast2['ds'].dt.month == datetime.now().month].iloc[0]
    
    # Create columns for metrics
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    
    with metric_col1:
        st.metric(label="This Month's Peak", value=f"{current_month_peak['yhat']:.2f} MWH")
    
    with metric_col2:
        st.metric(label="This Month's Avg Energy Requirement", value=f"{current_month_forecast['yhat']:.2f} MWH")

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

    with metric_col3:
       st.metric(label="Today's Avg Temperature", value=f"{avg_temp_today:.2f} °C" if avg_temp_today != 'Data not available' else avg_temp_today)

elif selection == "Coal Prices":
    st.header("Coal Prices")
    st.write("Here you can analyze and visualize coal prices. (Add your analysis code here.)")
    
elif selection == "Transmission Loss":
    st.header("Transmission Loss")
    st.write("Here you can analyze and visualize transmission loss data. (Add your analysis code here.)")
