"""
Names: Matthew, Bobby, Terry, Isaiah
Section: CS 230-7
Data: McDonald's Reviews
Description: This program allows users to analyze a large set of McDonald's
reviews by filtering through the data.
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

#Loads data:
df = pd.read_csv("McDonald_s_ReviewsFiltered.csv", encoding="ISO-8859-1")
df.rename(columns={'ï»¿Reviewer ID': 'Reviewer ID'}, inplace=True)
try:
    df["Rating"] = df["Rating"].astype(str).str.extract(r"(\d)").astype(int)
except Exception as e:
    st.warning(f"Rating column already formatted. Skipping conversion. ({e})")

df["Rating Count"] = pd.to_numeric(df["Rating Count"], errors='coerce').fillna(0).astype(int)

#[ST4]Displays page title and divider using HTML styling features:
col1, col2, col3 = st.columns([1, 8, 1])
with col2:
    st.markdown(
        "<p style='text-align: center; font-size:40px; color:red;'><b>McDonald's Reviews</b></p>",
        unsafe_allow_html=True
    )
st.divider()

#Displays full data table:
st.subheader("All Reviews")
st.dataframe(df, use_container_width=True)


st.subheader("Ratings Distribution")
#Matplotlib font and background setup:
plt.rcParams.update({
    "font.size": 8,
    "font.family": "sans-serif",
})

rating_counts = df['Rating'].value_counts().sort_index()
#Uses shades of red to match theme:
colors = ['#ffcccc', '#ff9999', '#ff6666', '#ff3333', '#cc0000']
#[CHART 1]Displays pie chart of ratings distribution:
fig, ax = plt.subplots(figsize=(3, 3), facecolor='#fff8e1')
ax.pie(
    rating_counts,
    labels=rating_counts.index,
    autopct='%1.1f%%',
    startangle=140,
    colors=colors[:len(rating_counts)],
    wedgeprops={'edgecolor': 'white'}
)
#Matches chart background color with page:
fig.patch.set_facecolor('#fff8e1')
st.pyplot(fig)


st.subheader("Map of Review Locations")
#[MAP]Displays map of all store locations:
map_data = df[['Latitude', 'Longitude']].dropna()
map_data.columns = ['lat', 'lon']
if not map_data.empty:
    st.map(map_data)
else:
    st.warning("No location data available.")

st.subheader("Most Popular Store Locations")
#[DA2]Sorts data in descending order by review count and stores the address and count:
top_stores = df.groupby("Store Address")["Rating Count"].max().sort_values(ascending=False).head(10)
st.write("Top 10 Stores by Review Count:")
st.dataframe(top_stores)