import streamlit as st
import pandas as pd

def createPage():
    st.markdown("### What others have been asking...")

    # Read in the csv file
    df = pd.read_csv('./files/logs.csv')

    # Define a function to create the accordion
    def accordion(answer, sources):
        with st.expander("Answer"):
            st.write(f"{answer}")
            st.write(f"Sources:\n {sources}")

    # Iterate through the rows of the dataframe and create an accordion for each row
    for index, row in df.iterrows():
        # Create two columns
        col1, col2 = st.columns([2, 3])
        
        # Add the question to the first column
        with col1:
            st.write(row['Question'])
        # Add the answer and sources to the second column
        with col2:
            accordion(row['Answer'], row['Sources'])
    return True