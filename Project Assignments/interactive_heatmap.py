import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# --- Instructions ---
# 1. This script generates a large, synthetic dataset (60,000 points) to demonstrate
#    the interactive time slider functionality across 60 months (Jan 2016 - Dec 2020).
# 2. To use your actual data, REPLACE the "Data Generation (MOCK)" section with
#    the "Actual Data Loading & Prep" section and ensure your data has a
#    'Start_Time' column in datetime format.
# 3. You will need Plotly, Pandas, and Numpy installed (pip install plotly pandas numpy).

# =================================================================
#                         1. DATA GENERATION (MOCK)
# =================================================================

START_DATE = datetime(2016, 1, 1)
END_DATE = datetime(2020, 12, 31)
NUM_POINTS = 60000 # Total number of mock accident records to generate

print(f"Generating a mock dataset of {NUM_POINTS} accident records over 60 months...")

# Calculate the duration in days
time_span_days = (END_DATE - START_DATE).days

# Generate random days within the time span
random_days = np.random.randint(0, time_span_days, NUM_POINTS)
# Calculate random timestamps
timestamps = [START_DATE + timedelta(days=int(d)) for d in random_days]

# Mock geospatial data (centered roughly on the US)
lat_center, lon_center = 38.0, -98.0
lat_spread, lon_spread = 15.0, 30.0

data = {
    'Start_Lat': np.clip(np.random.normal(lat_center, lat_spread / 4, NUM_POINTS), 25, 49),
    'Start_Lng': np.clip(np.random.normal(lon_center, lon_spread / 4, NUM_POINTS), -125, -67),
    'Start_Time': timestamps,
    'Severity': np.random.randint(1, 5, NUM_POINTS)
}
df = pd.DataFrame(data)

# Extract Year and Month (YYYY-MM) for the animation frame
df['Year_Month'] = df['Start_Time'].dt.to_period('M').astype(str)

# Sort the DataFrame by the animation frame column to ensure correct slider order
df = df.sort_values(by='Year_Month').reset_index(drop=True)

MONTH_FRAMES = sorted(df['Year_Month'].unique())

print(f"Mock data generation complete. Frames from {MONTH_FRAMES[0]} to {MONTH_FRAMES[-1]}.")

# =================================================================
#                         (OPTIONAL) ACTUAL DATA LOADING & PREP
# =================================================================
# If you have the real CSV file, uncomment and use this block instead:

# CSV_PATH = "Your_Accident_Data.csv"
# df = pd.read_csv(CSV_PATH)

# # 1. Ensure 'Start_Time' is a datetime object
# df['Start_Time'] = pd.to_datetime(df['Start_Time'])

# # 2. Filter for the requested period (2016-2020)
# df = df[df['Start_Time'].dt.year.between(2016, 2020)]

# # 3. Extract Year-Month for the animation frame
# df['Year_Month'] = df['Start_Time'].dt.to_period('M').astype(str)

# # 4. Sort and get unique frames
# df = df.sort_values(by='Year_Month').reset_index(drop=True)
# MONTH_FRAMES = sorted(df['Year_Month'].unique())

# # 5. Ensure required columns are present: 'Start_Lat', 'Start_Lng', 'Year_Month'
# df = df[['Start_Lat', 'Start_Lng', 'Year_Month']]
# =================================================================


# =================================================================
#                         2. PLOTLY VISUALIZATION
# =================================================================

print("Generating interactive Plotly figure...")

# Plotly Express density_mapbox is used with the new Year_Month column
fig = px.density_mapbox(
    df,
    lat='Start_Lat',
    lon='Start_Lng',
    # Use the YYYY-MM field for animation
    animation_frame='Year_Month',
    # Density and map properties
    radius=6,
    zoom=2.5,
    center=dict(lat=39.8, lon=-98.6),
    mapbox_style="carto-darkmatter", # Dark style enhances the color gradient
    color_continuous_scale="Hot", # A fiery color scale for "heatmap"
    title="US Traffic Accidents Heatmap: Monthly Trend (Jan 2016 - Dec 2020)"
)

# Customize Layout for a smoother slider experience
fig.update_layout(
    margin={"r":0,"t":50,"l":0,"b":0},
    coloraxis_colorbar=dict(
        title="Density",
        thicknessmode="pixels", thickness=20,
        lenmode="fraction", len=0.7,
        yanchor="middle", y=0.5,
        xanchor="left", x=0.02,
        ticks="outside",
    ),
    # Animation settings
    sliders=[
        dict(
            steps=[
                dict(
                    args=[
                        # Frame argument uses the Year_Month string
                        [y],
                        # Layout argument resets the plot for each step (smoother transition)
                        {'mapbox.layers': []}
                    ],
                    label=str(y),
                    method="animate"
                ) for y in MONTH_FRAMES
            ],
            transition=dict(duration=100, easing="linear"), # Faster, linear transition for smoothness
            x=0.08, y=0.02,
            len=0.84,
            currentvalue=dict(font=dict(size=14, color='white'), prefix="Date: ", visible=True, xanchor="right")
        )
    ]
)

# Set the play button's animation speed (1 second per frame)
fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 1000
fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 500

# Save the interactive figure as a stand-alone HTML file
output_file = "us_accidents_monthly_heatmap.html"
fig.write_html(output_file, auto_open=False)

print(f"\nSuccessfully generated interactive monthly heatmap: {output_file}")
print("Run the script and open the HTML file to view the interactive map with 60 steps on the slider.")
