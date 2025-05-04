#Imports libraries:
import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np
import re

#Sets page configuration to wide so elements span full page:
st.set_page_config(layout="wide")

#Loads and cleans the data:
df = pd.read_csv("McDonald_s_ReviewsFiltered.csv", encoding="ISO-8859-1")
df.rename(columns={'ï»¿Reviewer ID': 'Reviewer ID'}, inplace=True)
try:
    #[DA1]Manipulates data type for "Rating" column:
    df["Rating"] = df["Rating"].astype(str).str.extract(r"(\d)").astype(int)
except Exception as e:
    st.warning(f"Rating column already formatted. Skipping conversion. ({e})")

df["Rating Count"] = pd.to_numeric(df["Rating Count"], errors='coerce').fillna(0).astype(int)

#Extracts state info from address column:
df["State"] = df["Store Address"].str.extract(r",\s*([A-Z]{2})\s+\d{5}")

#[PY1]Function with two or more parameters:
#[PY2]Function that returns more than one value:
def filter_reviews(df, rating_range, keyword, selected_state):
    filtered = df[(df["Rating"] >= rating_range[0]) & (df["Rating"] <= rating_range[1])]
    if keyword:
        filtered = filtered[filtered["Review"].str.contains(keyword, case=False, na=False)]
    if selected_state != "All":
        filtered = filtered[filtered["State"] == selected_state]
    return filtered, len(filtered)

#Displays page title and divider:
col1, col2, col3 = st.columns([1, 8, 1])
with col2:
    st.markdown(
        "<p style='text-align: center; font-size:40px; color:red;'><b>Filtered McDonald's Reviews</b></p>",
        unsafe_allow_html=True
    )
st.divider()

#Displays sidebar controls:
st.sidebar.title("Filter Reviews")

#[DA4]Filters data by rating range:
#[ST2]Rating slider input:
ratingRange = st.sidebar.slider(
    "Select a rating range",
    min_value=1,
    max_value=5,
    value=(1, 5)
)

search_word = st.sidebar.text_input("Search for a keyword in reviews")

#Displays a list of suggested keywords below the search box:
suggested_keywords = ["service,", "clean,", "wait,", "friendly,", "slow"]
listOfWords = "Suggested keywords: "
for word in suggested_keywords:
    listOfWords += " "+word
st.sidebar.write(listOfWords)

#Creates a sorted list of states excluding missing ones:
state_options = ["All"] + sorted(df["State"].dropna().unique())
selected_state = st.sidebar.selectbox("Select a State:", state_options)

#[DA5]Applies multiple filters via function:
filtered_df, review_count = filter_reviews(df, ratingRange, search_word, selected_state)

#Displays total reviews matched:
st.caption(f"Total matching reviews: {review_count}")

#[CHART 2]Displays filtered data table:
st.subheader("Filtered Reviews")
st.dataframe(filtered_df, use_container_width=True)

#[MAP2]Displays heat map based on rating count:
filtered_df["Rating Count"] = filtered_df["Store Address"].map(filtered_df["Store Address"].value_counts())
map_data = filtered_df[['Latitude', 'Longitude', 'Rating Count']].dropna(subset=['Latitude', 'Longitude'])
map_data.columns = ['lat', 'lon', 'Rating Count']

if not map_data.empty:
    heatmap_layer = pdk.Layer(
        "HeatmapLayer",
        data=map_data,
        get_position='[lon, lat]',
        aggregation=pdk.types.String("SUM"),
        get_weight=2,
        radiusPixels=30,
    )

    midpoint = (np.average(map_data['lat']), np.average(map_data['lon']))

    heatmap_map = pdk.Deck(
        map_style="mapbox://styles/mapbox/dark-v10",
        initial_view_state=pdk.ViewState(
            latitude=midpoint[0],
            longitude=midpoint[1],
            zoom=4,
            pitch=40,
        ),
        layers=[heatmap_layer],
    )

    st.subheader("Review Heatmap")
    st.pydeck_chart(heatmap_map)
else:
    st.warning("No location data available for the selected filters.")