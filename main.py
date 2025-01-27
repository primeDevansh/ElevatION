import streamlit as st
import pandas as pd

cleanedSampleDataPath = 'sampleData/cleaned_sample_data.csv'
pagesPath = ['pages/1_profile.py',
             'pages/2_dashboard.py']

st.write("# ElevatION")
st.logo('Assets\LogoWithoutBG.webp', size='large')
st.image('Assets\LogoWithoutBG.webp', width=200)

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