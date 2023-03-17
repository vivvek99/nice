import streamlit as st
import pandas as pd

import styled_components as sc

df = pd.read_csv("conditions.csv")

styled = sc.styled
css = """
input {
    width: 100%;
    height: 40px;
    font-size: 18px;
    padding: 10px;
    margin-bottom: 20px;
    border: none;
    border-radius: 4px;
    box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.1);
}
"""
styled(css)(lambda: None)()

# Display the topics in a list with a search box
st.header("These are the topics on which this model has been trained")
with st.beta_container():
    search_term = st.text_input("Search for a topic")
    if search_term:
        filtered_df = df[df["Topic"].str.contains(search_term, case=False)]
    else:
        filtered_df = df
    for i, row in filtered_df.iterrows():
        topic = row["Topic"]
        st.write(f"{topic}")
