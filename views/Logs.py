import streamlit as st
import pandas as pd

def createPage():
    st.markdown("### What others have been asking...")

    # Read in the csv file
    df = pd.read_csv('./files/logs.csv')

    # Define a function to create the accordion
    def accordion(index, question, answer, sources):
        with st.expander(f"Question: {question}"):
            st.write(f"Answer: {answer}")
            st.write(f"Sources: {sources}")
            if st.button(f"Delete", key=f"delete_{index}"):
                df.drop(index, inplace=True)
                # Save the modified dataframe to the csv file
                df.to_csv('./files/logs.csv', index=False)
                st.experimental_rerun()

    # Iterate through the rows of the dataframe and create an accordion for each row
    for index, row in df[::-1].iterrows():
        accordion(index, row['Question'], row['Answer'], row['Sources'])
    

    return True
