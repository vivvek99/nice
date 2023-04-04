import streamlit as st
import pandas as pd

def createPage():
    st.markdown("### What others have been asking...")
    html_temp = """
                    <div style="background-color:{};padding:1px">
                    
                    </div>
                    """
    # with st.sidebar:
    #     st.markdown("""
    #     ### About 
    #     \nAsk any medical question and get an explanation. You can even clear your MCQ doubts.
    #     \nPlease note that a detailed question will get a detailed answer and will take 10-15 seconds.
    #     \n\nDisclaimer: **DO NOT** use as a substitute for professional medical advice. This is meant for **EDUCATIONAL PURPOSES ONLY**.
    #     \n### How does it work?
    #     \nIt is trained on NICE CKS guidelines as in https://cks.nice.org.uk
    #     \n*If the source is anything else other than NICE, then the answer could be wrong.*
    #     """)
    #     st.markdown("""[Source Code](https://github.com/faz-cxr/nice)
    #     <a href = "mailto:fazeen.nasser@outlook.com?subject = Feedback&body = Message">Send Feedback</a><br>
    #     <a href="https://www.buymeacoffee.com/fazeen" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-blue.png" alt="Buy Me A Coffee" style="height: 35px;width: 110px ;" ></a>
    #     """,
    #     unsafe_allow_html=True,
    #     )

    # Read in the csv file
    df = pd.read_csv('./files/logs.csv')

    # Define a function to create the accordion
    def accordion(answer, sources):
        with st.expander("Answer"):
            st.write(f"{answer}")
            st.write(f"Sources:\n {sources}")

    # Iterate through the rows of the dataframe and create an accordion for each row
    for index, row in df[::-1].iterrows():
        # Create two columns
        col1, col2 = st.columns([2, 3])
        
        # Add the question to the first column
        with col1:
            st.write(row['Question'])
        # Add the answer and sources to the second column
        with col2:
            accordion(row['Answer'], row['Sources'])
    return True