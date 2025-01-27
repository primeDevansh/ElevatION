import streamlit as st
import pandas as pd

cleanedSampleDataPath = 'sampleData/cleaned_sample_data.csv'
pagesPath = ['pages/1_profile.py',
             'pages/2_dashboard.py']
projectName = 'ElevatION'

# Set the page configuration to collapse the sidebar by default
st.set_page_config(
    page_title=projectName,
    page_icon="Assets/LogoWithoutBG.webp",
    initial_sidebar_state="collapsed"
)
st.title(projectName)
# Sidebar logo
st.logo('Assets/LogoWithoutBG.webp', size='large')

st.write("### What do we do?")
st.write("Let's add a link to our documentation and slide deck here?")

st.write("You can navigate between pages either through the sidebar or through links.")

st.page_link(pagesPath[0], label="Profile", icon='1️⃣')
st.page_link(pagesPath[1], label="Dashboard", icon='2️⃣')

# Extract company names as a list

# Input data into variable
data = pd.read_csv(cleanedSampleDataPath)

companies = data['ISSUERID'].unique().tolist()
no_companies = len(companies)
industries = data['IVA_INDUSTRY'].unique().tolist()
no_industries = len(industries)

company_selected = st.selectbox(
    "Select a copmany",
    companies,
    index=None,
    placeholder=f"Choose below out of {no_companies}",
)

if company_selected:
    st.write("You selected: ", company_selected)

st.write("### OR")

industry_selected = st.selectbox(
    "Select an industry",
    industries,
    index=None,
    placeholder=f"Choose below out of {no_industries}",
)