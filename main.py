import streamlit as st
from PIL import Image
import read_data # Ergänzen Ihr eigenes Modul

def callback_function():
    # Logging Message
    print(f"The user has changed to {st.session_state.current_user}")
    # Manuelles wieder ausführen
    #st.rerun()

if 'current_user' not in st.session_state:
    st.session_state.current_user = 'None'

if 'picture_path' not in st.session_state:
    st.session_state.picture_path = 'data/pictures/none.jpg'

person_dict = read_data.load_person_data()
person_names = read_data.get_person_list()
st.write("# EKG APP")

col1, col2 = st.columns(2)

with col1:
    st.write("## Versuchsperson auswählen")
    # Nutzen Sie ihre neue Liste anstelle der hard-gecodeten Lösung
    st.session_state.current_user = st.selectbox(
    'Versuchsperson',
        options = person_names, key="sbVersuchsperson", on_change = callback_function)

with col2:
    st.write("## Bild der Versuchsperson")
    if st.session_state.current_user in person_names:
        st.session_state.picture_path = read_data.find_person_data_by_name(st.session_state.current_user)["picture_path"]
    image = Image.open("./" + st.session_state.picture_path)
    st.image(image, caption=st.session_state.current_user)
