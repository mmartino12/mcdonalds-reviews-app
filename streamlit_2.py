import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# Generated with ChatGPT
# Set page title
st.title("Temperature Analysis")

# Load data
# datasource: currentresults.com
df = pd.read_excel("temp_data.xlsx")  # State, Avg_temp


# Approximate center coordinates for each US State
state_coords = {
    "Alabama": [32.806671, -86.791130],
    "Alaska": [61.370716, -152.404419],
    "Arizona": [33.729759, -111.431221],
    "Arkansas": [34.969704, -92.373123],
    "California": [36.116203, -119.681564],
    "Colorado": [39.059811, -105.311104],
    "Connecticut": [41.597782, -72.755371],
    "Delaware": [39.318523, -75.507141],
    "Florida": [27.766279, -81.686783],
    "Georgia": [33.040619, -83.643074],
    "Hawaii": [21.094318, -157.498337],
    "Idaho": [44.240459, -114.478828],
    "Illinois": [40.349457, -88.986137],
    "Indiana": [39.849426, -86.258278],
    "Iowa": [42.011539, -93.210526],
    "Kansas": [38.526600, -96.726486],
    "Kentucky": [37.668140, -84.670067],
    "Louisiana": [31.169546, -91.867805],
    "Maine": [44.693947, -69.381927],
    "Maryland": [39.063946, -76.802101],
    "Massachusetts": [42.230171, -71.530106],
    "Michigan": [43.326618, -84.536095],
    "Minnesota": [45.694454, -93.900192],
    "Mississippi": [32.741646, -89.678696],
    "Missouri": [38.456085, -92.288368],
    "Montana": [46.921925, -110.454353],
    "Nebraska": [41.125370, -98.268082],
    "Nevada": [38.313515, -117.055374],
    "New Hampshire": [43.452492, -71.563896],
    "New Jersey": [40.298904, -74.521011],
    "New Mexico": [34.840515, -106.248482],
    "New York": [42.165726, -74.948051],
    "North Carolina": [35.630066, -79.806419],
    "North Dakota": [47.528912, -99.784012],
    "Ohio": [40.388783, -82.764915],
    "Oklahoma": [35.565342, -96.928917],
    "Oregon": [44.572021, -122.070938],
    "Pennsylvania": [40.590752, -77.209755],
    "Rhode Island": [41.680893, -71.511780],
    "South Carolina": [33.856892, -80.945007],
    "South Dakota": [44.299782, -99.438828],
    "Tennessee": [35.747845, -86.692345],
    "Texas": [31.054487, -97.563461],
    "Utah": [40.150032, -111.862434],
    "Vermont": [44.045876, -72.710686],
    "Virginia": [37.769337, -78.169968],
    "Washington": [47.400902, -121.490494],
    "West Virginia": [38.491226, -80.954578],
    "Wisconsin": [44.268543, -89.616508],
    "Wyoming": [42.755966, -107.302490],
}

# Map the state names to coordinates
df['lat'] = df['State'].map(lambda x: state_coords.get(x, [None, None])[0])
df['lon'] = df['State'].map(lambda x: state_coords.get(x, [None, None])[1])

# Drop rows where lat/lon could not be found
df = df.dropna(subset=['lat', 'lon'])

#source: used ChatGPT to help create the slider function:
#Slider:
st.subheader("Temperature Range")
minTemp = round(df["Avg_temp"].min(), 1)
maxTemp = round(df["Avg_temp"].max(), 1)
tempRange = st.slider(
    "Select a temperature range (°F):",
    min_value=minTemp,
    max_value=maxTemp,
    value=(minTemp, maxTemp)
)

filtered_df = df[(df["Avg_temp"] >= tempRange[0]) & (df["Avg_temp"] <= tempRange[1])]


# Display the raw data
st.subheader("Raw Temperature Data")
st.dataframe(filtered_df)

# Show the map
st.subheader("Temperature Map")

# Define the layer
layer = pdk.Layer(
    "ScatterplotLayer",
    data=filtered_df,
    get_position='[lon, lat]',
    get_color='[255, (1 - Avg_temp/100)*255, 0, 160]',  # color changes with temp
    get_radius=50000,
    pickable=True,
    tooltip=True
)

# Define the view
view_state = pdk.ViewState(
    latitude=37.0902,
    longitude=-95.7129,
    zoom=3,
    pitch=0
)

# Create the map
r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "{State}\nAvg Temp: {Avg_temp}°F"}
)

st.pydeck_chart(r)

# ======================================================================================
# Optional: Plot temperature distribution
st.subheader("Temperature Distribution Plot")
fig, ax = plt.subplots()
sns.histplot(filtered_df['Avg_temp'], bins=20, kde=False, ax=ax)
ax.set_xlabel('Average Temperature (°F)')
ax.set_ylabel('Frequency')
ax.set_title('Distribution of Average Temperatures')
st.pyplot(fig)
# ======================================================================================

st.subheader("NumPy Temperature Analysis")

avg_temps = filtered_df['Avg_temp'].to_numpy()  # Convert Avg_temp column to a NumPy array

mean_temp = np.mean(avg_temps)
median_temp = np.median(avg_temps)
std_temp = np.std(avg_temps)

st.write(f"**Mean Temperature:** {mean_temp:.2f} °F")
st.write(f"**Median Temperature:** {median_temp:.2f} °F")
st.write(f"**Standard Deviation:** {std_temp:.2f} °F")

