import pandas as pd
import numpy as np

class EKGdata:
    def __init__(self, id, date, result_link):
        """
        Initialize the EKGdata object with the given id, date, and result link.
        
        Parameters:
        - id: Unique identifier for the EKG test.
        - date: Date of the EKG test.
        - result_link: Link to the CSV file containing EKG data.
        """
        self.id = id
        self.date = date
        self.result_link = result_link
        
        # Read the EKG data from the CSV file
        self.df = pd.read_csv(result_link, sep="\t", names=["EKG in mV","Time in ms"])
        
        # Find peaks in the EKG data
        self.df_with_peaks, self.peaks = EKGdata.find_peaks(self, self.df)
        
        # Estimate heart rate from the EKG data
        self.df_with_hr = EKGdata.estimate_hr_dataset(self)

    def find_peaks(self, series, threshold=350):
        """
        Find peaks in the EKG data that exceed a given threshold.
        
        Parameters:
        - series: DataFrame containing the EKG data.
        - threshold: Value above which a peak is considered significant.
        
        Returns:
        - series: DataFrame with an additional column indicating peaks.
        - peaks: List of indices where peaks occur.
        """
        ekg_values = series["EKG in mV"].values
        peaks = []
        
        # Iterate through the EKG values to find peaks
        for i in range(1, len(ekg_values) - 1):
            if ekg_values[i] > ekg_values[i - 1] and ekg_values[i] > ekg_values[i + 1] and ekg_values[i] > threshold:
                peaks.append(i)
                
        peaks_index = pd.Index(peaks, dtype=int)
        series["Peaks"] = np.nan
        series.loc[peaks_index, "Peaks"] = series.loc[peaks_index, "EKG in mV"]
        
        return series, peaks
    
    def estimate_hr_dataset(self):
        """
        Estimate the heart rate from the EKG data by calculating intervals between peaks.
        
        Returns:
        - series_with_peaks: DataFrame with an additional column for estimated heart rate.
        """
        series_with_peaks, peaks = self.df_with_peaks, self.peaks
        series_with_peaks["HeartRate"] = np.nan
        
        # Calculate intervals between peaks
        peak_intervals = np.diff(peaks)
        sampling_rate = 1000  # Assuming data is in milliseconds
        heart_rates = 60 / (peak_intervals / sampling_rate)
        
        # Assign heart rate values to corresponding peaks
        for i, peak in enumerate(peaks[1:], start=1):
            series_with_peaks.at[peak, "HeartRate"] = heart_rates[i-1]
            
        return series_with_peaks
    
    @staticmethod
    def load_by_id(id, person_dict):
        """
        Load EKG data by ID from a given person's record.
        
        Parameters:
        - id: Unique identifier for the EKG test.
        - person_dict: Dictionary containing the person's EKG test records.
        
        Returns:
        - df: DataFrame containing the EKG data if the ID is found, otherwise an empty dictionary.
        """
        if id == "None":
            return {}
        
        for eintrag in person_dict["ekg_tests"]:
            if eintrag["id"] == id:
                df = pd.read_csv(eintrag["result_link"], sep="\t", names=["EKG in mV","Time in ms"])
                return df
        
        return {}
    
    @staticmethod
    def estimate_max_hr(age_years: int, sex: str) -> int:
        """
        Estimate the maximum heart rate based on age and sex.
        
        Parameters:
        - age_years: Age of the person in years.
        - sex: Sex of the person ('male' or 'female').
        
        Returns:
        - max_hr_bpm: Estimated maximum heart rate in beats per minute.
        
        References:
        - See https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4124545/ for different formulas.
        """
        if sex == "male":
            max_hr_bpm = 223 - 0.9 * age_years
        elif sex == "female":
            max_hr_bpm = 226 - 1.0 * age_years
        else:
            raise ValueError("Invalid sex. Please specify 'male' or 'female'.")
        
        return int(max_hr_bpm)
