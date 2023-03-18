import streamlit as st
import pandas as pd

df = pd.read_csv("conditions.csv")

# Display the topics in a list with a search box
st.markdown("### These are the topics on which this model has been trained on")

html_temp = """
                <div style="background-color:{};padding:1px">
                
                </div>
                """

with st.sidebar:
    st.markdown("""
    ### About 
    \nAsk any medical question and get an explanation. You can even clear your MCQ doubts.
    \nPlease note that a detailed question will get a detailed answer and will take 10-15 seconds.
    \n\nDisclaimer: **DO NOT** use as a substitute for professional medical advice. This is meant for **EDUCATIONAL PURPOSES ONLY**.
    """)
    st.markdown(html_temp.format("rgba(55, 53, 47, 0.16)"),unsafe_allow_html=True)
    st.markdown("""
    ### How does it work?
    \nIt is trained on NICE CKS guidelines as in https://cks.nice.org.uk
    \n*If the source is anything else other than NICE, then the answer could be wrong.*
    """)
    st.markdown(html_temp.format("rgba(55, 53, 47, 0.16)"),unsafe_allow_html=True)
    st.markdown("""
    <a href = "mailto:fazeen.nasser@outlook.com?subject = Feedback&body = Message">Send Feedback</a>
    """,
    unsafe_allow_html=True,
    )
    st.markdown("""
    <a href="https://www.buymeacoffee.com/fazeen" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-blue.png" alt="Buy Me A Coffee" style="height: 35px;width: 110px ;" ></a>
    """,
    unsafe_allow_html=True,
    )
    
with st.beta_container():
    st.write(" ")
    search_term = st.text_input("Search topics:")
    if search_term:
        filtered_df = df[df["Topic"].str.contains(search_term, case=False)].reset_index(drop=True)
    else:
        filtered_df = df.reset_index(drop=True)
    for i, row in filtered_df.iterrows():
        topic = row["Topic"]
        ref = row["Ref"]
        st.write(f"{i+1}. [{topic}]({ref})")
    st.write(" ")
