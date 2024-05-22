import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def read_my_csv():
    # Einlesen eines Dataframes
    column_names = ["HeartRate", "Duration", "PowerOriginal"]
    df = pd.read_csv("activity.csv", sep=",", header=0, usecols=column_names)
    df["Duration"] = df.index
    # Gibt den geladenen Dataframe zurück
    return df

def mean_power(df):
    return df['PowerOriginal'].mean()

def max_power(df):
    return df['PowerOriginal'].max()

def calculate_time_in_zones(df, max_heart_rate):
    zones = [
        {"min": 0, "max": 0.6 * max_heart_rate, "color": "lightgreen", "label": "Zone 1"},
        {"min": 0.6 * max_heart_rate, "max": 0.7 * max_heart_rate, "color": "yellow", "label": "Zone 2"},
        {"min": 0.7 * max_heart_rate, "max": 0.8 * max_heart_rate, "color": "orange", "label": "Zone 3"},
        {"min": 0.8 * max_heart_rate, "max": 0.9 * max_heart_rate, "color": "red", "label": "Zone 4"},
        {"min": 0.9 * max_heart_rate, "max": max_heart_rate, "color": "darkred", "label": "Zone 5"}
    ]
    
    time_in_zones = []
    average_power_in_zones = []

    for zone in zones:
        zone_data = df[(df['HeartRate'] >= zone['min']) & (df['HeartRate'] < zone['max'])]
        time_spent = len(zone_data)
        average_power = zone_data['PowerOriginal'].mean() if not zone_data.empty else 0
        time_in_zones.append(time_spent)
        average_power_in_zones.append(average_power)

    return time_in_zones, average_power_in_zones

# Funktion zum Erstellen des Plots
def make_plot(df, max_heart_rate, time_in_zones, average_power_in_zones):
    # Definieren der Herzfrequenzzonen
    zones = [
        {"min": 0, "max": 0.6 * max_heart_rate, "color": "lightgreen", "label": "Zone 1"},
        {"min": 0.6 * max_heart_rate, "max": 0.7 * max_heart_rate, "color": "yellow", "label": "Zone 2"},
        {"min": 0.7 * max_heart_rate, "max": 0.8 * max_heart_rate, "color": "orange", "label": "Zone 3"},
        {"min": 0.8 * max_heart_rate, "max": 0.9 * max_heart_rate, "color": "red", "label": "Zone 4"},
        {"min": 0.9 * max_heart_rate, "max": max_heart_rate, "color": "darkred", "label": "Zone 5"}
    ]
    
    fig = go.Figure()

    # Add PowerOriginal line to the left y-axis
    fig.add_trace(go.Scatter(x=df["Duration"], y=df["PowerOriginal"], name="PowerOriginal", yaxis="y1"))

    # Add HeartRate line to the right y-axis
    fig.add_trace(go.Scatter(x=df["Duration"], y=df["HeartRate"], name="HeartRate", yaxis="y2"))

    # Set up layout with two y-axes
    fig.update_layout(
        title="Heart Rate and PowerOriginal by Zone",
        xaxis_title="Duration",
        yaxis=dict(
            title="PowerOriginal",
            titlefont=dict(color="blue"),
            tickfont=dict(color="blue")
        ),
        yaxis2=dict(
            title="HeartRate",
            titlefont=dict(color="red"),
            tickfont=dict(color="red"),
            anchor="x",
            overlaying="y",
            side="right"
        ),
        legend=dict(x=1.1, y=1.1)
    )

    # Add background shapes for zones
    for i, zone in enumerate(zones):
        fig.add_shape(
            type="rect",
            x0=df["Duration"].min(), x1=df["Duration"].max(),
            y0=zone["min"], y1=zone["max"],
            fillcolor=zone["color"],
            opacity=0.2,
            line_width=0,
            layer="below",
            yref="y2"  # Reference to the right y-axis (HeartRate)
        )
        
        # Adding zone labels
        fig.add_annotation(
            x=df["Duration"].max(),
            y=(zone["min"] + zone["max"]) / 2,
            text=f"{zone['label']}",
            showarrow=False,
            yshift=10,
            bgcolor="rgba(255,255,255,0.5)",
            yref="y2"  # Reference to the right y-axis (HeartRate)
        )

    return fig

def calculate_resting_heart_rate(activity_data):
    # Wir nehmen an, dass die niedrigsten 5% der Herzfrequenzwerte die Ruheherzfrequenz darstellen
    resting_heart_rate = activity_data['HeartRate'].nsmallest(int(len(activity_data) * 0.05)).mean()
    return resting_heart_rate

def create_zones_table(time_in_zones, average_power_in_zones):
    zones_df = pd.DataFrame({
        "Zone": ["Zone 1", "Zone 2", "Zone 3", "Zone 4", "Zone 5"],
        "Time (s)": time_in_zones,
        "Average Power (W)": average_power_in_zones
    })
    return zones_df

if __name__ == "__main__":
    df = read_my_csv()
    max_heart_rate = df['HeartRate'].max()
    fig = make_plot(df, max_heart_rate)
    fig.show()
