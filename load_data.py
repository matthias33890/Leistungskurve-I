import psycopg2
import pandas as pd
import json

# Verbindung zur Datenbank herstellen
conn = psycopg2.connect(
    dbname="your_dbname", user="your_user", password="your_password", host="your_host", port="your_port"
)
cur = conn.cursor()

def person_exists(person_id):
    cur.execute("SELECT 1 FROM persons WHERE id = %s", (person_id,))
    return cur.fetchone() is not None

def ekgdata_exists(ekg_id):
    cur.execute("SELECT 1 FROM ekgdata WHERE id = %s", (ekg_id,))
    return cur.fetchone() is not None

def load_person_data(person_dict):
    if not person_exists(person_dict["id"]):
        cur.execute("""
            INSERT INTO persons (id, firstname, lastname, date_of_birth, picture_path, age, max_heartrate)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            person_dict["id"],
            person_dict["firstname"],
            person_dict["lastname"],
            person_dict["date_of_birth"],
            person_dict["picture_path"],
            person_dict["age"],
            person_dict["max_heartrate"]
        ))
        conn.commit()

def load_ekg_data(ekg_dict):
    if not ekgdata_exists(ekg_dict["id"]):
        df = pd.read_csv(ekg_dict["result_link"], sep="\t", names=["EKG in mV", "Time in ms"])
        df_json = df.to_json(orient='records')
        
        # Diese Funktionen müssen definiert werden, um die peaks und df_with_hr zu erhalten
        df_with_peaks_json, peaks_json = calculate_peaks_and_hr(df)

        cur.execute("""
            INSERT INTO ekgdata (id, person_id, date, result_link, df, df_with_peaks, peaks, df_with_hr, plot)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            ekg_dict["id"],
            ekg_dict["person_id"],
            ekg_dict["date"],
            ekg_dict["result_link"],
            df_json,
            df_with_peaks_json,
            peaks_json,
            df_with_hr_json,
            None  # plot muss separat behandelt werden
        ))
        conn.commit()

def calculate_peaks_and_hr(df):
    # Platzhalter für die Berechnung von Peaks und df_with_hr
    # Diese Funktion sollte die Datenframe-Berechnungen durchführen und die Ergebnisse als JSON zurückgeben
    df_with_peaks = df  # Beispiel
    peaks = []  # Beispiel
    df_with_hr = df  # Beispiel
    return df_with_peaks.to_json(orient='records'), json.dumps(peaks), df_with_hr.to_json(orient='records')

# Daten laden
with open('person_db.json', 'r') as f:
    persons = json.load(f)
    for person_dict in persons:
        load_person_data(person_dict)
        for ekg_test in person_dict["ekg_tests"]:
            ekg_test["person_id"] = person_dict["id"]
            load_ekg_data(ekg_test)

# Verbindung schließen
cur.close()
conn.close()
