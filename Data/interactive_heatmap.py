import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta


# =================================================================
#                 1. DATA LOADING AND PREPARATION
# =================================================================
df_map = pd.read_csv("Data/us_accidents_sample_500k_clean.csv")

# 1. Ensure 'Start_Time' is a datetime object
df_map['Start_Time'] = pd.to_datetime(df_map['Start_Time'])

# 2. Filter for the requested period (2016-2020)
df_map = df_map[df_map['Start_Time'].dt.year.between(2016, 2023)]

# 3. Extract Year-Month for the animation frame
df_map['Year_Month'] = df_map['Start_Time'].dt.to_period('M').astype(str)

# 4. Sort and get unique frames
df_map = df_map.sort_values(by='Year_Month').reset_index(drop=True)
MONTH_FRAMES = sorted(df_map['Year_Month'].unique())
# 5. Ensure required columns are present: 'Lat', 'Lng', 'Year_Month'
df_map = df_map[['Lat', 'Lng', 'Year_Month']]

# =================================================================
#                         2. PLOTLY VISUALIZATION
# =================================================================

print("Generating interactive Plotly figure...")

# Plotly Express density_mapbox is used with the new Year_Month column
fig = px.density_mapbox(
    df_map ,
    lat='Lat',
    lon='Lng',
    # Use the YYYY-MM field for animation
    animation_frame='Year_Month',
    # Density and map properties
    radius=6,
    zoom=2.5,
    center=dict(lat=39.8, lon=-98.6),
    mapbox_style="carto-darkmatter", 
    color_continuous_scale="Hot", 
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
    # Animation 
    sliders=[
        dict(
            steps=[
                dict(
                    args=[
                        # Frame argument uses the Year_Month string
                        [y],
                        # Layout argument resets the plot for each step
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

# Save the interactive figure as a HTML file
output_file = "us_accidents_monthly_heatmap.html"
fig.write_html(output_file, auto_open=False)

print(f"\nSuccessfully generated interactive monthly heatmap: {output_file}")