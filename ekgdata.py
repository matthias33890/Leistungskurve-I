import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy import signal
import numpy as np
from plotly import subplots


class EKGdata:
    def __init__(self, id, date, result_link):
        self.id = id
        self.date = date
        self.result_link = result_link
        self.df = pd.read_csv(result_link, sep="\t", names=["EKG in mV","Time in ms"])
        self.df_with_peaks, self.peaks = EKGdata.find_peaks(self, self.df)
        self.df_with_hr = EKGdata.estimate_hr_dataset(self)

    def find_peaks(self, series, threshold=350):
        ekg_values = series["EKG in mV"].values
        peaks = []
        for i in range(1, len(ekg_values) - 1):
            if ekg_values[i] > ekg_values[i - 1] and ekg_values[i] > ekg_values[i + 1] and ekg_values[i] > threshold:
                peaks.append(i)
        peaks_index = pd.Index(peaks, dtype=int)
        series["Peaks"] = np.nan
        series.loc[peaks_index, "Peaks"] = series.loc[peaks_index, "EKG in mV"]
        return series, peaks
    
    def estimate_hr_dataset(self):
        series_with_peaks, peaks = self.df_with_peaks, self.peaks
        series_with_peaks["HeartRate"] = np.nan
        peak_intervals = np.diff(peaks)
        sampling_rate = 1000 
        heart_rates = 60 / (peak_intervals / sampling_rate)
        for i, peak in enumerate(peaks[1:], start=1):
            series_with_peaks.at[peak, "HeartRate"] = heart_rates[i-1]      
        return series_with_peaks
    
    


    @staticmethod
    def load_by_id(id, person_dict):
        """ Eine Funktion der ID und die Person als Dictionary übergeben wird und anschließend die EKG-Daten zurück gibt"""
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
    def estimate_max_hr(age_years : int , sex : str) -> int:
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