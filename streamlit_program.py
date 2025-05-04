# Generated with ChatGPT
#To rerun code each time: ctrl c --> up arrow to get run command previously used

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Welcome to Fashion Reviews Analysis")

df = pd.read_excel("example_data.xlsx")

#New functionality added:
st.header ("Review Rating Breakdown")
rating_counts = df["Rating"].value_counts().sort_index()
fig2, ax2 = plt.subplots()
ax2.pie(rating_counts.values,labels = rating_counts.index,
        autopct='%1.1f%%',
        startangle =90,
        counterclock=False)
ax2.axis("equal")
st.pyplot(fig2)

#--------------------------------------------
st.header("Counts for each Rating")

# Count the number of reviews for each rating
rating_counts = df['Rating'].value_counts().sort_index()
# Create the plot
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(rating_counts.index, rating_counts.values)
ax.set_xlabel('Star Rating')
ax.set_ylabel('Number of Reviews')
ax.set_title('Number of Reviews per Star Rating')
ax.set_xticks([1, 2, 3, 4, 5])
ax.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig)

# --------------------------------------------------------------------------------------------------------
st.header("Rating Ranges")

rating_range = st.slider("Select Rating Range", 1, 5, (1, 5))
filtered_df = df[df['Rating'].between(rating_range[0], rating_range[1])]
st.dataframe(filtered_df)

# ---------------------------------------------------------------------------------------------------------
st.header("Search Reviews by Keyword")

keyword = st.text_input("Enter a keyword to search in review text")


if keyword:
    keyword_reviews = df[df['ReviewText'].str.contains(keyword, case=False, na=False)]

    count = len(keyword_reviews)
    st.write(f"🔎 Found {count} reviews containing **'{keyword}'**")

    if count > 0:
        avg_rating = keyword_reviews['Rating'].mean()
        st.write(f" Average Rating: {avg_rating:.2f}")

        st.subheader("Sample Reviews")
        for i, review in enumerate(keyword_reviews['ReviewText'].sample(min(3, count))):
            st.markdown(f"**{i+1}.** {review}")
    else:
        st.warning("No matching reviews found.")

#-------------------

