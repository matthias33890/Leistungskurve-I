import streamlit as st
from read_pandas import read_my_csv
from read_pandas import make_plot
from read_pandas import mean_power
from read_pandas import max_power
from read_pandas import calculate_resting_heart_rate
from read_pandas import create_zones_table
from read_pandas import calculate_time_in_zones

tab1, tab2 = st.tabs(["Graph", "Data"])
df = read_my_csv()

with tab1:
    st.header("Graph")
    max_heart_rate = st.number_input('Maximale Herzfrequenz', min_value=100, max_value=220, value=190) 
    time_in_zones, average_power_in_zones = calculate_time_in_zones(df, max_heart_rate)
    zones_table = create_zones_table(time_in_zones, average_power_in_zones)
    fig = make_plot(df, max_heart_rate,time_in_zones, average_power_in_zones)
    st.plotly_chart(fig)

with tab2:
    st.header("Data")
    st.write("Mean Power: ", df['PowerOriginal'].mean())
    st.write("Max Power: ", df['PowerOriginal'].max())
    st.write("Resting Heart Rate: ", calculate_resting_heart_rate(df))
    st.write("Max Heart Rate: ", df['HeartRate'].max())
    st.write("Time and Average Power in Zones")
    st.dataframe(zones_table)
