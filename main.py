import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from math import pi
import plotly.graph_objects as go
from datetime import datetime

cleanedSampleDataPath = 'sampleData/cleaned_sample_data.csv'
pagesPath = ['pages/1_profile.py',
             'pages/2_dashboard.py']

def create_radar_chart(data, categories, title):
    N = len(categories)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    plt.xticks(angles[:-1], categories)

    values = data.tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle='solid')
    ax.fill(angles, values, 'b', alpha=0.1)

    plt.title(title)

    st.pyplot(fig)

def convert_date(date):
    date_str = str(int(date))
    date_formatted = pd.to_datetime(date_str, format='%Y%m%d').strftime('%Y-%m-%d')
    return date_formatted


projectName = 'ElevatION'
# Set the page configuration to collapse the sidebar by default
st.set_page_config(
    page_title=projectName,
    page_icon="Assets/LogoWithBG.png",
    initial_sidebar_state="collapsed",
    layout="wide",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
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
    "Select a company",
    companies,
    index=None,
    placeholder=f"Choose below out of {no_companies}",
)

if company_selected:
    st.write("You selected: ", company_selected)

# st.write("### OR")

# industry_selected = st.selectbox(
#     "Select an industry",
#     industries,
#     index=None,
#     placeholder=f"Choose below out of {no_industries}",
# )

if company_selected != None:
    # st.balloons()
    # Load your dataset
    df = pd.read_csv(cleanedSampleDataPath)

    # Filter data for the selected company
    company_data = df[df['ISSUERID'] == company_selected]

    # 1. ESG Rating
    # Get the rating and date
    rating = company_data['IVA_COMPANY_RATING'].values[0]
    rating_date = convert_date(company_data['IVA_RATING_DATE'].values[0])

    # Define color coding based on rating
    if rating in ['AAA', 'AA']:
        color = '#166352'  # Green
    elif rating in ['BB', 'BBB', 'A']:
        color = '#FBA600'  # Yellow
    elif rating in ['CCC', 'B']:
        color = '#BD1C2B'  # Red
    else:
        color = 'gray'  # Default color for unexpected values

    # Display the rating with color coding
    st.markdown(f"""
        <div style='background-color: {color}; padding: 10px; border-radius: 5px; text-align: center;'>
            <strong style='font-size: 16px;'>Company Rating: {rating}</strong><br>
            <strong style='font-size: 14px;'>Rating Date: {rating_date}</strong>
        </div>
        """, unsafe_allow_html=True)

    st.write(" ")

    # 2. Individual-ESG Scores as Radar Plot
    # Arrange plots in a grid layout
    col1, col2, col3 = st.columns(3)
    categories = ['ENVIRONMENTAL_PILLAR_SCORE', 'SOCIAL_PILLAR_SCORE', 'GOVERNANCE_PILLAR_SCORE']
    data = company_data[categories].mean()
    with col1:
        create_radar_chart(data, categories, 'ESG Scores')

    # 3. Pie chart for corporate governance and behavior scores
    gov_behavior_scores = company_data[['CORP_BEHAV_SCORE', 'BOARD_SCORE', 'PAY_SCORE', 'TAX_TRANSP_GOV_PILLAR_SD']].mean()
    fig, ax = plt.subplots()
    gov_behavior_scores.plot(kind='pie', autopct='%1.1f%%', ax=ax)
    ax.set_ylabel('')
    ax.set_title('Corporate Governance and Behavior Scores')
    with col2:
        st.pyplot(fig)

    # 4. Theme Scores as bar plot
    theme_scores = company_data[['CLIMATE_CHANGE_THEME_SCORE', 'BUSINESS_ETHICS_THEME_SCORE', 'HUMAN_CAPITAL_THEME_SCORE', 'NATURAL_RES_USE_THEME_SCORE', 'WASTE_MGMT_THEME_SCORE']].mean()
    fig, ax = plt.subplots()
    theme_scores.plot(kind='bar', ax=ax)
    ax.set_title('Theme Scores')
    ax.set_ylabel('Score')
    with col3:
        st.pyplot(fig)

    # 5. Risk and Opportunity Score as Gauge Plot
    # Arrange plots in a grid layout
    col4, col5, col6 = st.columns(3)
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=company_data['WATER_STRESS_SCORE'].values[0],
        title={'text': "Water Stress Score"},
        gauge={
            'axis': {'range': [0, 10]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 2.5], 'color': "red"},
                {'range': [2.5, 5], 'color': "orange"},
                {'range': [5, 7.5], 'color': "yellow"},
                {'range': [7.5, 10], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': company_data['WATER_STRESS_SCORE'].values[0]
            }
        }
    ))
    with col4:
        st.plotly_chart(fig)

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=company_data['TOXIC_EMISS_WSTE_SCORE'].values[0],
        title={'text': "Toxic Emissions and Waste Score"},
        gauge={
            'axis': {'range': [0, 10]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 2.5], 'color': "red"},
                {'range': [2.5, 5], 'color': "orange"},
                {'range': [5, 7.5], 'color': "yellow"},
                {'range': [7.5, 10], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': company_data['WATER_STRESS_SCORE'].values[0]
            }
        }
    ))
    with col5:
        st.plotly_chart(fig)