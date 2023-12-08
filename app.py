import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="🚕 Taxifare by OS",  # => Quick reference - Streamlit
    page_icon="🚕",
    layout="wide",  # wide
    initial_sidebar_state="collapsed")  # collapsed
'''
# 🚕 Welcome to my TaxiFare!
'''
columns = st.columns(2)

columns[0].markdown("### Pickup time")

date = columns[0].date_input("Please select a pickup date")
time = columns[0].time_input(
    "Please select your pickup time (US/Eastern time)")

columns[0].markdown("### Pickup location")

pickup_lon = columns[0].number_input(
    "Please select a pickup longitude", value=5.377147392612483)
pickup_lat = columns[0].number_input(
    "Please select a pickup latitude", value=43.29449193743676)

columns[0].markdown("### Dropoff location")

dropoff_lon = columns[0].number_input(
    "Please select a dropoff longitude", value=5.419846881072489)
dropoff_lat = columns[0].number_input(
    "Please select a dropoff latitude", value=43.21013513403245)

columns[0].markdown('### Passengers')
passengers = columns[0].number_input(
    label="Please select the number of passengers", step=0, min_value=1, max_value=8)


def get_map_data():
    return pd.DataFrame({
        'lat': [pickup_lat, dropoff_lat],
        'lon': [pickup_lon, dropoff_lon]
    })


columns[1].map(get_map_data(), zoom=11)

if columns[1].button("➡️ Get my taxi fare"):
    URL = 'https://taxifare.lewagon.ai/predict'
    params = dict(
        pickup_datetime=f"{date} {time}",
        pickup_longitude=pickup_lon,
        pickup_latitude=pickup_lat,
        dropoff_longitude=dropoff_lon,
        dropoff_latitude=dropoff_lat,
        passenger_count=passengers)
    result = requests.get(URL, params).json()
    fare = round(result["fare"], 2)
    columns[1].write(f"# 💵 ${fare+passengers}")
    st.balloons()
    if fare > 1000:
        columns[1].write("⚠️ C'est beaucoup d'argent")
