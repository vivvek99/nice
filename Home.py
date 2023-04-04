import streamlit as st 
from streamlit_option_menu import option_menu
from views import App, Conditions, Logs, About

st.set_page_config(
    page_title="Ask NICEly CKS!", 
    page_icon=":brain:", 
    #layout="wide"
    )

v_menu=["Ask NICE", "About", "Conditions", "Logs",]

selected = option_menu(
    menu_title=None,
    options=v_menu,
    icons=["robot","info-circle","list-ol","activity"],
    menu_icon="menu-down",
    default_index=0,
    orientation="horizontal"
)

if selected=="Ask NICE":
    App.createPage()

if selected=="About":
    About.createPage()

if selected=="Conditions":
    Conditions.createPage()

if selected=="Logs":
    Logs.createPage()