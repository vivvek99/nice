import streamlit as st 
from streamlit_option_menu import option_menu
from views import App, Conditions, Logs

st.set_page_config(page_title="Ask NICEly CKS!", page_icon=":brain:", layout="wide")

v_menu=["Ask NICE", "Conditions", "Logs"]

with st.sidebar:

    selected = option_menu(
        menu_title=None,
        options=v_menu,
        icons=["robot","list-ol","send"],
        menu_icon="menu-down",
        default_index=0,
    )

if selected=="Ask NICE":
    App.createPage()

if selected=="Conditions":
    Conditions.createPage()

if selected=="Logs":
    Logs.createPage()