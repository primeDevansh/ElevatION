import streamlit as st

st.write("# Dashboard")

projectName = 'ElevatION'
# Set the page configuration to collapse the sidebar by default
st.set_page_config(
    page_title=projectName,
    page_icon="../Assets/LogoWithBG.png",
    initial_sidebar_state="collapsed",
)

st.page_link("main.py", label="Back")