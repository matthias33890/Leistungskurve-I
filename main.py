import plotly.subplots
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from PIL import Image
from person import Person
from ekgdata import EKGdata
import plotly

#Lastenheft für Abschlussprojekt:
# Basistodo:
# Code schöner strukturieren
# Readmed verbessern
# Basisfunktionen fertig implementieren
#
# Zusätzliche Funktionen:
# Schneller laden indem ich di serie in st.sessionstat speicher bzw. auf einer Datenbank speichern
# schneller machen durch multiple-core
# Auf Hostinger schlussendlich in einem Docker hosten, sodaß es auch von außen erreichbar ist
# 
########################################################################################

def callback_function():
    print(f"The user has changed to {st.session_state.current_user}")
    print(f"The EKG date has changed to {st.session_state.ekg_date}")

if 'current_user' not in st.session_state:
    st.session_state.current_user = 'None'

if 'picture_path' not in st.session_state:
    st.session_state.picture_path = 'data/pictures/none.jpg'

person_dict = Person.load_person_data()
person_names = Person.get_person_list(person_dict)
st.write("# EKG APP")

col1, col2 = st.columns(2)

with col1:
    st.write("## Versuchsperson auswählen")
    # Nutzen Sie ihre neue Liste anstelle der hard-gecodeten Lösung
    st.session_state.current_user = st.selectbox('Versuchsperson',
        options = person_names, key="sbVersuchsperson", on_change = callback_function)
    current_person_dict = Person.find_person_data_by_name(st.session_state.current_user)


with col2:
    st.write("## Bild der Versuchsperson")
    if st.session_state.current_user in person_names:
        st.session_state.picture_path = Person.find_person_data_by_name(st.session_state.current_user)["picture_path"]
        current_person_dict = Person.find_person_data_by_name(st.session_state.current_user)
    image = Image.open("./" + st.session_state.picture_path)
    st.image(image, caption=st.session_state.current_user)

st.write("## EKG Daten")
ekg_data = current_person_dict["ekg_tests"]
ekg_dates = [ekg["date"] for ekg in ekg_data]

st.session_state.current_date = st.selectbox('Experimentauswahl',
        options = ekg_dates, key="sbExperimentauswahl", on_change = callback_function)

ekg_data = [ekg for ekg in ekg_data if ekg["date"] == st.session_state.current_date]
ekg_data = ekg_data[0]

current_ekg = EKGdata(int(ekg_data["id"]), ekg_data["date"], ekg_data["result_link"])
#Entweder vom Objekt die df verwenden, ich verwende jetzt aber load_by_id damit dies auch verwendet wird
ekg_df = current_ekg.load_by_id(ekg_data["id"], current_person_dict)

st.write("## EKG Diagramm")

#st.write("Peaks", current_ekg.find_peaks(ekg_df))
if 'result' not in st.session_state:
    # Schätze die Herzfrequenz und speichere das Ergebnis im Session State
    st.session_state.result = current_ekg.estimate_hr_dataset(ekg_df, threshold=350)

result = st.session_state.result
#fig = current_ekg.plot_time_series(ekg_df)
#fig.add_trace(go.Scatter(x=peaks, y=ekg_df['EKG in mV'].iloc[peaks], mode='markers', name='Peaks', marker=dict(color='red', size=10)))

# Plotten der Daten mit Plotly
fig = plotly.subplots.make_subplots(rows=2, cols=1, shared_xaxes=True,
                    subplot_titles=('EKG Signal', 'Heart Rate'))

# Plot EKG Signal
fig.add_trace(go.Scatter(x=result.index, y=result["EKG in mV"], mode='lines', name='EKG in mV'),
              row=1, col=1)
# Plot Peaks
fig.add_trace(go.Scatter(x=result.index, y=result["Peaks"], mode='markers', name='Peaks', marker=dict(color='red')),
              row=1, col=1)

# Plot Heart Rate (nur an den Positionen der Peaks)
fig.add_trace(go.Scatter(x=result.index, y=result["HeartRate"], mode='markers', name='Heart Rate', marker=dict(color='blue')),
              row=2, col=1)

# Verbinde die Herzfrequenzwerte nur an den Peaks
peak_indices = result.dropna(subset=["HeartRate"]).index
fig.add_trace(go.Scatter(x=peak_indices, y=result.loc[peak_indices, "HeartRate"], mode='lines', name='Heart Rate (Line)', line=dict(color='green')),
              row=2, col=1)

# Update Layout
fig.update_layout(height=600, width=800, title_text="EKG Signal and Heart Rate")
fig.update_xaxes(title_text="Time", row=2, col=1)
fig.update_yaxes(title_text="EKG in mV", row=1, col=1)
fig.update_yaxes(title_text="Heart Rate (BPM)", row=2, col=1)
st.plotly_chart(fig, use_container_width=True)

st.write("## Parameter")
st.write("Max Heartrate",current_ekg.estimate_max_hr(Person.calc_age(current_person_dict["date_of_birth"]), "male"))

st.write("Durchschnittswert in mV", ekg_df["EKG in mV"].mean())