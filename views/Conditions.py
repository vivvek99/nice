import streamlit as st
import pandas as pd

df = pd.read_csv("./files/conditions.csv")
def createPage():
    # Display the topics in a list with a search box
    st.markdown("### AskNICE is finely tuned to answer these topics.")
        
    with st.container():
        st.write(" ")
        search_term = st.text_input("Search topics:")
        if search_term:
            filtered_df = df[df["Topic"].str.contains(search_term, case=False)].reset_index(drop=True)
        else:
            filtered_df = df[::-1].reset_index(drop=True)
        for i, row in filtered_df.iterrows():
            topic = row["Topic"]
            ref = row["Ref"]
            st.write(f"{i+1}. [{topic}]({ref})")
        st.write(" ")
    return True
