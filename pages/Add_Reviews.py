#Imports libraries:
import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np
import re

#Loads and cleans the data:
df = pd.read_csv("McDonald_s_ReviewsFiltered.csv", encoding="ISO-8859-1")
#Fixes a name issue for the first column header:
df.rename(columns={'ï»¿Reviewer ID': 'Reviewer ID'}, inplace=True)
try:
    df["Rating"] = df["Rating"].astype(str).str.extract(r"(\d)").astype(int)
except Exception as e:
    st.warning(f"Rating column already formatted. Skipping conversion. ({e})")
df["Rating Count"] = pd.to_numeric(df["Rating Count"], errors='coerce').fillna(0).astype(int)

#Displays page title and divider:
col1, col2, col3 = st.columns([1, 8, 1])
with col2:
    st.markdown(
        "<p style='text-align: center; font-size:40px; color:red;'><b>Submit a McDonald's Review</b></p>",
        unsafe_allow_html=True
    )
st.divider()

#[DA7]Creates list to store each unique store location:
uniqueAddresses = []
for address in df["Store Address"]:
    if address not in uniqueAddresses:
        uniqueAddresses.append(address)

#User inputs:
#[ST1]Dropdown menu for store address selection:
selectedAddress = st.selectbox("Store address: ", uniqueAddresses)
selectedRating = st.select_slider("Rating:", options = [1, 2, 3, 4, 5])
#[ST3]Text input for writing a review:
newReview = st.text_area("Review: ")

#Submit review button:
if st.button("Submit Review"):
    #Non-inputs:
    newReviewerID = max(df["Reviewer ID"]) + 1
    store_row = df[df["Store Address"] == selectedAddress].iloc[0]
    newLatitude = store_row["Latitude"]
    newLongitude = store_row["Longitude"]
    newRatingTime = "0 days ago"
    #[PY4]Adds the data to a new dictionary and accesses keys:
    newRecord = {
        "Reviewer ID": newReviewerID,
        "Store Address": selectedAddress,
        "Latitude": newLatitude,
        "Longitude": newLongitude,
        "Rating Count": 0,
        "Rating Time": newRatingTime,
        "Review": newReview,
        "Rating": selectedRating
    }

    #Appends new review:
    df = pd.concat([df, pd.DataFrame([newRecord])], ignore_index=True)
    #[DA9] Recalculates Rating Count for all reviews based on store address:
    df["Rating Count"] = df["Store Address"].map(df["Store Address"].value_counts())

    #Saves new record to csv file:
    df.to_csv("McDonald_s_ReviewsFiltered.csv", index = False, encoding="ISO-8859-1")
    st.success("Review submitted!")