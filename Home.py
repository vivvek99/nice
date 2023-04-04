import streamlit as st 
from streamlit_option_menu import option_menu
from views import App, Conditions, Logs, About

st.set_page_config(
    page_title="Ask NICEly CKS!", 
    page_icon=":brain:", 
    #layout="wide"
    )

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

v_menu=["Ask", "About", "Logs", "Conditions"]

selected = option_menu(
    menu_title=None,
    options=v_menu,
    icons=["robot","info-circle","activity","list-ol"],
    menu_icon="menu-down",
    default_index=0,
    orientation="horizontal"
)

if selected=="Ask":
    App.createPage()

if selected=="About":
    About.createPage()

if selected=="Logs":
    Logs.createPage()

if selected=="Conditions":
    Conditions.createPage()