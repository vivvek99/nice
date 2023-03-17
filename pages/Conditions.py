import streamlit as st
import pandas as pd

df = pd.read_csv("conditions.csv")

st.header("These are the conditions on which the model has been trained on")
with st.beta_container():
    st.write(" ")
    search_term = st.text_input("Search for a topic:")
    if search_term:
        filtered_df = df[df["Topic"].str.contains(search_term, case=False)]
    else:
        filtered_df = df
    for i, row in filtered_df.iterrows():
        topic = row["Topic"]
        st.write(f"{topic}")
    st.write(" ")
