import streamlit as st
import pandas as pd

df = pd.read_csv("conditions.csv")

st.header("These are the conditions on which the model has been trained on")
with st.beta_container():
    st.write(" ")
    for i, condition in enumerate(df["Topic"], start=1):
        st.write(f"{i}. {condition}", unsafe_allow_html=True)
    st.write(" ")
