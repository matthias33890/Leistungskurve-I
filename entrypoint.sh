#!/bin/bash
# Warte auf die Datenbank, bevor setup.py ausgeführt wird und streamlit startet

# Prüfe die Datenbankverbindung
until pg_isready -h db -p 5432 -U user; do
  echo "Warte auf PostgreSQL..."
  sleep 2
done

# Führe setup.py aus
python setup.py

# Starte Streamlit
streamlit run main.py
