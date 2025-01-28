import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from math import pi
from datetime import datetime
import matplotlib.pyplot as plt

cleanedSampleDataPath = 'sampleData/sample_with_names.csv'
pagesPath = ['pages/1_Profile.py', 'pages/2_Dashboard.py', 'pages/3_Consolidated.py', 'pages/4_GetHelp.py']
helpPageIndex=3

def create_radar_chart(data, categories, title):
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=data.tolist() + [data.tolist()[0]],
        theta=categories + [categories[0]],
        fill='toself'
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True)
        ),
        showlegend=False,
        title=title
    )
    st.plotly_chart(fig)

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
    # menu_items={
    #     'Get Help': pagesPath[helpPageIndex],
    #     'Report a bug': pagesPath[helpPageIndex],
    #     'About': pagesPath[helpPageIndex],
    # }
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

companies = data['CompanyName'].unique().tolist()
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
    company_data = df[df['CompanyName'] == company_selected]

    ##### DISPLAY INDUSTRY INFORMATION
    col1, col2, col3 = st.columns(3)

    # Display the text in each column
    with col1:
        st.write(f"Industry Cluster: {company_data['Industry']}")
    with col2:
        st.write(f"Exact Industry: {company_data['IVA_INDUSTRY']}")
    with col3:
        st.write(f"Sub-Industry: {company_data['GICS_SUB_IND']}")

        
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
    fig = go.Figure(data=[go.Pie(labels=gov_behavior_scores.index, values=gov_behavior_scores.values)])
    fig.update_layout(title='Corporate Governance and Behavior Scores')
    with col2:
        st.plotly_chart(fig)

    # 4. Theme Scores as bar plot
    theme_scores = company_data[['CLIMATE_CHANGE_THEME_SCORE', 'BUSINESS_ETHICS_THEME_SCORE', 'HUMAN_CAPITAL_THEME_SCORE', 'NATURAL_RES_USE_THEME_SCORE', 'WASTE_MGMT_THEME_SCORE']].mean()
    fig = go.Figure(data=[go.Bar(x=theme_scores.index, y=theme_scores.values)])
    fig.update_layout(title='Theme Scores', yaxis_title='Score')
    with col3:
        st.plotly_chart(fig)

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

    # TEST
    # Calculate average ESG scores per industry
    # esg_scores = df.groupby('IVA_INDUSTRY')[['ENVIRONMENTAL_PILLAR_SCORE', 'SOCIAL_PILLAR_SCORE', 'GOVERNANCE_PILLAR_SCORE']].mean()

    # # Plot the stacked bar chart
    # esg_scores.plot(kind='bar', stacked=True)
    # with col6:
    #     st.pyplot(plt)