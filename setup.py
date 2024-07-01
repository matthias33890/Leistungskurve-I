import psycopg2
from psycopg2 import sql
from psycopg2.extras import Json
from person import Person
from ekgdata import EKGdata
import json
import pandas as pd

# Hole die Datenbank-URL aus den Umgebungsvariablen
database_url = "postgresql://leistungs_user:password@localhost:5432/leistungskurve"
conn = psycopg2.connect(database_url)
cur = conn.cursor()

def create_tables():
    commands = (
        """
        CREATE TABLE IF NOT EXISTS persons (
            id SERIAL PRIMARY KEY,
            firstname VARCHAR(50),
            lastname VARCHAR(50),
            date_of_birth INT,
            picture_path VARCHAR(255),
            age INT,
            max_heartrate INT,
            person_dict JSONB
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS ekgdata (
            id SERIAL PRIMARY KEY,
            person_id INT REFERENCES persons(id),
            date DATE,
            result_link VARCHAR(255),
            df JSONB,
            df_with_peaks JSONB,
            df_with_hr JSONB
        )
        """
    )
    try:
        # Tabellen erstellen
        for command in commands:
            cur.execute(command)
        # Änderungen speichern
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def person_exists(person_id):
    cur.execute("SELECT 1 FROM persons WHERE id = %s", (person_id,))
    return cur.fetchone() is not None

def ekgdata_exists(ekg_id):
    cur.execute("SELECT 1 FROM ekgdata WHERE id = %s", (ekg_id,))
    return cur.fetchone() is not None

def convert_df_to_json(df):
    # Ersetze NaN-Werte durch None für die JSON-Konvertierung
    df_replaced = df.where(pd.notnull(df), None)
    return df_replaced.to_json(orient='records')

def load_data():
    person_dict = Person.load_person_data()
    for person in person_dict:
        current_person = Person(person)
        person_dict_json = json.dumps(current_person.person_dict)
        
        if not person_exists(current_person.id):
            cur.execute("""
                INSERT INTO persons (id, firstname, lastname, date_of_birth, picture_path, age, max_heartrate, person_dict)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                current_person.id,
                current_person.firstname, current_person.lastname,
                current_person.date_of_birth,
                current_person.picture_path,
                current_person.age,
                current_person.max_heartrate,
                Json(current_person.person_dict)
            ))
            conn.commit()
            print(f"Person {current_person.firstname} {current_person.lastname} hinzugefügt.")
        
        ekg_data = person["ekg_tests"]
        for ekg in ekg_data:
            current_ekg = EKGdata(ekg["id"], ekg["date"], ekg["result_link"])
            if not ekgdata_exists(current_ekg.id):
                cur.execute("""
                    INSERT INTO ekgdata (id, person_id, date, result_link, df, df_with_peaks, df_with_hr)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    current_ekg.id,
                    current_person.id,
                    current_ekg.date,
                    current_ekg.result_link,
                    Json(convert_df_to_json(current_ekg.df)),
                    Json(convert_df_to_json(current_ekg.df_with_peaks)),
                    Json(convert_df_to_json(current_ekg.df_with_hr))
                ))
                conn.commit()
                print(f"EKG-Daten für Person {current_person.firstname} {current_person.lastname} hinzugefügt.")

if __name__ == '__main__':
    create_tables()
    load_data()
    cur.close()
    conn.close()
