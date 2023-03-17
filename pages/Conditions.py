import streamlit as st
import pandas as pd

import streamlit.components.v1 as components

df = pd.read_csv("conditions.csv")

st.header("These are the conditions on which the model has been trained on")
with st.beta_container():
    st.write(" ")
    search_term = components.ace(
        key="search",
        placeholder="Search for a topic",
        language="text",
        height=50,
        font_size=14,
        show_gutter=False,
        show_print_margin=False,
        wrap=True,
    )
    if search_term:
        filtered_df = df[df["Topic"].str.contains(search_term, case=False)]
    else:
        filtered_df = df
    for i, row in filtered_df.iterrows():
        topic = row["Topic"]
        st.write(f"{topic}")
    st.write(" ")
