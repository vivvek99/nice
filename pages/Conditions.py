import streamlit as st
import pandas as pd

df = pd.read_csv("conditions.csv")

# Display the topics in a list with a search box
st.header("These are the topics on which this model has been trained")
with st.beta_container():
    st.write(" ")
    search_term = st.text_input("Search topics:")
    if search_term:
        filtered_df = df[df["Topic"].str.contains(search_term, case=False)]
    else:
        filtered_df = df
    counter = 1
    for i, row in filtered_df.iterrows():
        topic = row["Topic"]
        st.write(f"{counter}. {topic}")
        counter += 1
    st.write(" ")
