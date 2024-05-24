import streamlit as st
from read_pandas import read_my_csv
from read_pandas import make_plot
from read_pandas import mean_power
from read_pandas import max_power
from read_pandas import calculate_resting_heart_rate
from read_pandas import create_zones_table
from read_pandas import calculate_time_in_zones
from read_pandas import extract_power_time_at
import plotly.express as px
import plotly.graph_objects as go

tab1, tab2, tab3, tab4 = st.tabs(["Graph-Power/Heartrate", "Data Heartrate/Power", "Data Leistungskurve-II", "Graph Leistungskurve-II"])
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

with tab3:
    st.subheader("DataFrame")
    result_df = extract_power_time_at(df)
    st.dataframe(result_df)

with tab4:
    st.subheader("Leistungskurve-II")
    fig = px.line(result_df, y='Threshold', x='Durations', title='Durations per Threshold', labels={'Threshold': 'Threshold in Watt', 'Durations': 'Durations in Seconds'})
    st.plotly_chart(fig)