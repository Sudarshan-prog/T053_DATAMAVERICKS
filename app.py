import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from streamlit_autorefresh import st_autorefresh
import pytz


# ThingSpeak settings
CHANNEL_ID = '2850551'
READ_API_KEY = 'B3PZCWWK9I3Q3163'
LOCAL_TIMEZONE = 'UTC'

# Function to fetch data from ThingSpeak with caching
@st.cache_data(ttl=60)  # Cache data for 60 seconds
def fetch_data():
    url = f'https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?api_key={READ_API_KEY}&results=100'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['feeds']:
            df = pd.DataFrame(data['feeds'])
            df['created_at'] = pd.to_datetime(df['created_at'])
            df['Voltage'] = pd.to_numeric(df['field1'], errors='coerce')
            df['Current'] = pd.to_numeric(df['field2'], errors='coerce')
            df['Power'] = pd.to_numeric(df['field3'], errors='coerce')
            df['Energy'] = pd.to_numeric(df['field4'], errors='coerce')
            return df.dropna()
    return pd.DataFrame()

# Set the autorefresh interval in milliseconds (e.g., 60000ms for 1 minute)
st_autorefresh(interval=6000, key="data_refresh")

# Streamlit app
st.title('Real-Time IoT Dashboard')
st.subheader('Monitoring Voltage, Current, Power, and Energy')

# Fetch and display data
data = fetch_data()
if not data.empty:
    latest_data = data.iloc[-1]
    st.write(f"Last updated: {latest_data['created_at']}")

    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Voltage (V)", f"{latest_data['Voltage']:.2f}")
    col2.metric("Current (A)", f"{latest_data['Current']:.2f}")
    col3.metric("Power (W)", f"{latest_data['Power']:.2f}")
    col4.metric("Energy (kwh)", f"{latest_data['Energy']:.2f}")

    # Plot graphs
    st.subheader('Historical Data')
    fig_voltage = px.line(data, x='created_at', y='Voltage', title='Voltage over Time')
    st.plotly_chart(fig_voltage, use_container_width=True)

    fig_current = px.line(data, x='created_at', y='Current', title='Current over Time')
    st.plotly_chart(fig_current, use_container_width=True)

    fig_energy = px.line(data, x='created_at', y='Energy', title='Power over Time')
    st.plotly_chart(fig_energy, use_container_width=True)

    fig_power = px.line(data, x='created_at', y='Power', title='Energy over Time')
    st.plotly_chart(fig_power, use_container_width=True)
else:
    st.warning("Failed to retrieve data.")
