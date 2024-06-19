import plotly.subplots
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from PIL import Image
from person import Person
from ekgdata import EKGdata
import plotly

#Pflichtenheft für Abschlussprojekt:
# Basistodo:
# Code schöner strukturieren
# EKG-Daten werden beim Einlesen sinnvoll resampelt, um Ladezeiten zu verkürzen (2pkt)
# Nutzer:in kann sinnvollen Zeitbereich für Plots auswählen (2pkt)
# Kommentare und Docstrings (2pkt)
# Deployment auf Heroku oder Streamlit Sharing (2pkt)
# Person weniger Statische methoden
#
# Zusätzliche Funktionen: max 24 pkt
# Schneller laden indem man die serie in st.sessionstat speicher bzw. auf einer Datenbank speichern (6pt)
# schneller machen durch multiple-core 2-4pkt
# Auf Hostinger schlussendlich in einem Docker hosten, sodaß es auch von außen erreichbar ist 8pkt
# Als Dockercontainer zur Verfügung stellen 4 pkt
# Als Webapp zur Verfügung stellen 4 pkt
# 
########################################################################################

def callback_function():
    print(f"The user has changed to {st.session_state.current_user}")
    print(f"The EKG date has changed to {st.session_state.ekg_dates}")

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
    st.session_state.current_user = st.selectbox('Versuchsperson',
        options = person_names, key="sbVersuchsperson", on_change = callback_function)
    current_person_dict = Person.find_person_data_by_name(st.session_state.current_user)
    st.write("Geburtsjahr: ", current_person_dict["date_of_birth"])
    ekg_data = current_person_dict["ekg_tests"]
    ekg_dates = [ekg["date"] for ekg in ekg_data]

    st.session_state.current_date = st.selectbox('Experimentauswahl',
            options = ekg_dates, key="sbExperimentauswahl", on_change = callback_function)

    ekg_data = [ekg for ekg in ekg_data if ekg["date"] == st.session_state.current_date]
    ekg_data = ekg_data[0]

    current_ekg = EKGdata(int(ekg_data["id"]), ekg_data["date"], ekg_data["result_link"])
    #Entweder vom Objekt die df verwenden, ich verwende jetzt aber load_by_id damit dies auch verwendet wird
    st.write('Länge der Zeitreihe in Sekunden:', (current_ekg.df["Time in ms"].max() - current_ekg.df["Time in ms"].min())/ 1000)

with col2:
    st.write("### Bild der Versuchsperson")
    if st.session_state.current_user in person_names:
        st.session_state.picture_path = Person.find_person_data_by_name(st.session_state.current_user)["picture_path"]
        current_person_dict = Person.find_person_data_by_name(st.session_state.current_user)
    image = Image.open("./" + st.session_state.picture_path)
    st.image(image, caption=st.session_state.current_user)

st.write("### EKG Diagramm")
st.write("Max Heartrate",current_ekg.estimate_max_hr(Person.calc_age(current_person_dict["date_of_birth"]), "male"))

st.write("Durchschnittswert in mV", current_ekg.df["EKG in mV"].mean())
#st.write("Peaks", current_ekg.find_peaks(ekg_df))
if 'result' not in st.session_state:
    # Schätze die Herzfrequenz und speichere das Ergebnis im Session State
    st.session_state.result = current_ekg.df_with_hr

result = st.session_state.result

fig = current_ekg.plot_time_series()
st.plotly_chart(fig, use_container_width=True)

