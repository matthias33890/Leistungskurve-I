import streamlit as st
import psycopg2
from psycopg2.extras import Json
from PIL import Image
from person import Person
import pandas as pd
import json
import plotly.graph_objects as go
from plotly import subplots
import time
from concurrent.futures import ThreadPoolExecutor

# Datenbankverbindung herstellen
database_url = "postgresql://leistungs_user:password@localhost:5432/leistungskurve"
conn = psycopg2.connect(database_url)
cur = conn.cursor()

# Callback-Funktion
def callback_function():
    st.session_state.current_user = st.session_state.sbVersuchsperson
    st.session_state.current_date = st.session_state.sbExperimentauswahl
    st.experimental_rerun()

# Initialisiere die Session State
if 'current_user' not in st.session_state:
    st.session_state.current_user = 'None'

if 'picture_path' not in st.session_state:
    st.session_state.picture_path = 'data/pictures/none.jpg'

# Lade Personendaten aus der Datenbank
def load_person_data():
    cur.execute("SELECT * FROM persons")
    rows = cur.fetchall()
    persons = []
    for row in rows:
        person_dict_str = row[7] if isinstance(row[7], str) else json.dumps(row[7])
        person = {
            "id": row[0],
            "firstname": row[1],
            "lastname": row[2],
            "date_of_birth": row[3],
            "picture_path": row[4],
            "age": row[5],
            "max_heartrate": row[6],
            "person_dict": json.loads(person_dict_str)
        }
        persons.append(person)
    return persons

# Lade EKG-Daten aus der Datenbank
def load_ekg_data_by_person_id(person_id):
    cur.execute("SELECT * FROM ekgdata WHERE person_id = %s", (person_id,))
    rows = cur.fetchall()
    ekg_tests = []
    for row in rows:
        ekg = {
            "id": row[0],
            "person_id": row[1],
            "date": row[2],
            "result_link": row[3],
            "df": pd.read_json(row[4]),
            "df_with_peaks": pd.read_json(row[5]),
            "df_with_hr": pd.read_json(row[6])
        }
        ekg_tests.append(ekg)
    return ekg_tests

person_dict = load_person_data()
person_names = [f"{person['firstname']} {person['lastname']}" for person in person_dict]

st.write("# EKG APP")

col1, col2 = st.columns(2)
with col1:
    st.write("## Versuchsperson auswählen")
    st.session_state.current_user = st.selectbox('Versuchsperson',
        options=person_names, key="sbVersuchsperson", on_change=callback_function)
    
    current_person_dict = next(person for person in person_dict if f"{person['firstname']} {person['lastname']}" == st.session_state.current_user)
    current_person = Person(current_person_dict)
    st.write("Geburtsjahr: ", current_person_dict["date_of_birth"])
    
    with ThreadPoolExecutor() as executor:
        future_ekg_data = executor.submit(load_ekg_data_by_person_id, current_person.id)
        ekg_data = future_ekg_data.result()

    ekg_dates = [ekg["date"] for ekg in ekg_data]

    st.session_state.current_date = st.selectbox('Experimentauswahl',
            options=ekg_dates, key="sbExperimentauswahl", on_change=callback_function)

    ekg_data = next(ekg for ekg in ekg_data if ekg["date"] == st.session_state.current_date)

    current_ekg_df = ekg_data["df"]
    current_ekg_df_with_peaks = ekg_data["df_with_peaks"]
    current_ekg_df_with_hr = ekg_data["df_with_hr"]
    
    st.write('Länge der Zeitreihe in Minuten:', (current_ekg_df["Time in ms"].max() - current_ekg_df["Time in ms"].min()) / 60000)

with col2:
    st.write("### Bild der Versuchsperson")
    if st.session_state.current_user in person_names:
        st.session_state.picture_path = current_person_dict["picture_path"]
    image = Image.open("./" + st.session_state.picture_path)
    st.image(image, caption=st.session_state.current_user)

st.write("### EKG Diagramm")
# Schieberegler für den Zeitbereich
min_time = current_ekg_df["Time in ms"].min() / 60000
max_time = current_ekg_df["Time in ms"].max() / 60000
start_time, end_time = st.slider(
    'Wählen Sie den anzuzeigenden Zeitbereich (in Minuten)',
    min_value=min_time,
    max_value=max_time,
    value=(min_time+3, max_time-3)
)

st.write("Max Heartrate", current_person_dict["max_heartrate"])
st.write("Durchschnittswert in mV", current_ekg_df["EKG in mV"].mean())

if 'result' not in st.session_state:
    st.session_state.result = current_ekg_df_with_hr

result = st.session_state.result

def plot_time_series(min_time, max_time):
    # Filtere die Daten basierend auf min_time und max_time
    filtered_df = result[(result["Time in ms"] / 60000 >= min_time) & (result["Time in ms"] / 60000 <= max_time)]
    
    fig = subplots.make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.2)
    
    # Plot EKG Signal
    fig.add_trace(go.Scattergl(x=filtered_df["Time in ms"] / 60000, y=filtered_df["EKG in mV"], mode='lines', name='EKG in mV'),
                  row=1, col=1)
    
    # Plot Peaks
    fig.add_trace(go.Scattergl(x=filtered_df["Time in ms"] / 60000, y=filtered_df["Peaks"], mode='markers', name='Peaks', marker=dict(color='red')),
                  row=1, col=1)
    
    # Plot Heart Rate (nur an den Positionen der Peaks)
    fig.add_trace(go.Scattergl(x=filtered_df["Time in ms"] / 60000, y=filtered_df["HeartRate"], mode='markers', name='Heart Rate', marker=dict(color='blue')),
                  row=2, col=1)
    
    # Verbinde die Herzfrequenzwerte nur an den Peaks
    peak_indices = filtered_df.dropna(subset=["HeartRate"]).index
    fig.add_trace(go.Scattergl(x=filtered_df.loc[peak_indices, "Time in ms"] / 60000, y=filtered_df.loc[peak_indices, "HeartRate"], mode='lines', name='Heart Rate (Line)', line=dict(color='green')),
                  row=2, col=1)
    
    # Update Layout
    fig.update_layout(height=600, width=800, title_text="EKG Signal and Heart Rate")
    fig.update_xaxes(title_text="Time in minutes", row=2, col=1)
    fig.update_yaxes(title_text="EKG in mV", row=1, col=1)
    fig.update_yaxes(title_text="Heart Rate (BPM)", row=2, col=1)
    return fig

# Plotten der gesamten Daten
fig = plot_time_series(start_time, end_time)
st.plotly_chart(fig, use_container_width=True)

# Schließe die Verbindung
cur.close()
conn.close()
