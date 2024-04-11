import pandas as pd
import matplotlib.pyplot as plt
import os #erstellt Ordner, Directorys etc.
from sort import bubble_sort
from load_data import load_data
def main():
    # Lade die CSV-Datei
    #data = pd.read_csv('Sort_activity.csv') # weitere Möglichkeit die Daten zu laden

    data = load_data('Sort_activity.csv')
    print(data)
    # Überprüfe, ob die Spalte 'PowerOriginal' vorhanden ist
    if 'PowerOriginal' not in data.keys():
        print("Die Spalte 'PowerOriginal' fehlt in den Daten.")
        return

    # Entferne NaN-Werte und sortiere die Werte
    #sorted_power_1 = data['PowerOriginal'].dropna().sort_values() # weitere möglichkeit die Werte zu sortieren
    power = data['PowerOriginal']
    sorted_power = bubble_sort(power)
    print(sorted_power[::-1]) #mit [::-1] wird die Liste umgedreht
    
    plt.figure()
    # Umwandlung der Indexwerte von Sekunden in Minuten
    minutes = range(len(sorted_power))  # Erzeugt eine Sequenz von Indizes
    minutes = [m / 60 for m in minutes]  # Konvertiert Indizes in Minuten

    plt.plot(minutes, sorted_power[::-1], label='PowerOriginal')
    plt.title('Power-Curve')
    plt.xlabel('Minuten')
    plt.ylabel('Leistung (Watt)')
    plt.legend()

    # Überprüfe, ob der Ordner 'figures' existiert, und erstelle ihn ggf.
    if not os.path.exists('figures'):
        os.makedirs('figures')

    # Speichere die Grafik
    plt.savefig('figures/power_curve.png')

    print("Die Grafik wurde in 'figures/power_curve.png' gespeichert.")

if __name__ == '__main__':
    main()


