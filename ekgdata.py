import json
import pandas as pd
from person import Person
import plotly.express as px
import plotly.graph_objects as go
from scipy import signal
import numpy as np
# Klasse EKG-Data für Peakfinder, die uns ermöglicht peaks zu finden
class EKGdata:
## Konstruktor der Klasse soll die Daten einlesen
    def __init__(self, id, date, result_link):
        self.id = id
        self.date = date
        self.result_link = result_link
        self.df = pd.read_csv(result_link, sep="\t", names=["EKG in mV","Time in ms"])

    @staticmethod
    def load_by_id(id, person_dict):
        """ Eine Funktion der ID und die Person als Dictionary übergeben wird und anschließend die EKG-Daten zurück gibt"""
        #print(suchstring)
        if id == "None":
            return {}
        for eintrag in person_dict["ekg_tests"]:
            print(eintrag)
            if eintrag["id"] == id:
                print()
                df = pd.read_csv(eintrag["result_link"], sep="\t", names=["EKG in mV","Time in ms"])
                return df
        else:
            return {}
    @staticmethod
    def find_peaks(series, threshold=350):
        ekg_values = series["EKG in mV"].values
        peaks = []
        for i in range(1, len(ekg_values) - 1):
            if ekg_values[i] > ekg_values[i - 1] and ekg_values[i] > ekg_values[i + 1] and ekg_values[i] > threshold:
                peaks.append(i)
        peaks_index = pd.Index(peaks, dtype=int)
        series["Peaks"] = np.nan
        series.loc[peaks_index, "Peaks"] = series.loc[peaks_index, "EKG in mV"]

        return series, peaks
    @staticmethod
    def estimate_hr_dataset(series, threshold=350):
        series_with_peaks, peaks = EKGdata.find_peaks(series, threshold)
        series_with_peaks["HeartRate"] = np.nan
        peak_intervals = np.diff(peaks)
        sampling_rate = 1000 
        heart_rates = 60 / (peak_intervals / sampling_rate)
        for i, peak in enumerate(peaks[1:], start=1):
            series_with_peaks.at[peak, "HeartRate"] = heart_rates[i-1]      
        return series_with_peaks

    def estimate_max_hr(self, age_years : int , sex : str) -> int:
        """
        See https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4124545/ for different formulas
        """
        if sex == "male":
            max_hr_bpm =  223 - 0.9 * age_years
        elif sex == "female":
            max_hr_bpm = 226 - 1.0 *  age_years
        else:
            print("Ein Fehler ist aufgetreten")
        return int(max_hr_bpm)

    def plot_time_series(self, df):
        # Definieren der Herzfrequenzzonen
        fig = go.Figure()
        # linke y-Achse für PowerOriginal
        fig.add_trace(go.Scatter(x=df["Time in ms"], y=df["EKG in mV"], name="EKG in mV"))
        return fig

if __name__ == "__main__":
    print("This is a module with some functions to read the EKG data")
    file = open("data/person_db.json")
    person_data = json.load(file)
    ekg_dict = person_data[0]["ekg_tests"][0]
    print(ekg_dict)
    ekg = EKGdata(ekg_dict)
    print(ekg.df.head())
