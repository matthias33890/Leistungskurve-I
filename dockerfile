# Verwende ein offizielles Python-Runtime-Image als Basis
FROM python:3.9

# Setze das Arbeitsverzeichnis im Container
WORKDIR /app

# Kopiere requirements.txt und installiere Python-Abhängigkeiten
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den restlichen Projektinhalt in das Arbeitsverzeichnis
COPY . .

# Exponiere den Standard-Port für Streamlit
EXPOSE 8501

# Führe setup.py aus, um die Datenbanktabellen zu erstellen, wenn der Container gestartet wird
CMD ["bash", "entrypoint.sh"]
