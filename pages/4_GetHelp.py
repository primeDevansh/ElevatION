import streamlit as st

pageName = 'Get Help'
# Set the page configuration to collapse the sidebar by default
st.set_page_config(
    page_title="ElevatION",
    page_icon="Assets/LogoWithBG.png",
    initial_sidebar_state="collapsed",
    layout="wide",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    },
)

st.title(pageName)
# Sidebar logo
st.logo('Assets/LogoWithoutBG.webp', size='large')

st.page_link("main.py", label="Home")