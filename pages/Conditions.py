import streamlit as st
import pandas as pd

df = pd.read_csv("conditions.csv")

st.header("These are the conditions on which the model has been trained on")
for condition in df["Topic"]:
    st.write("- " + condition)
