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

    # Define the features for each category
    environmental_features = [
        'ENVIRONMENTAL_PILLAR_SCORE', 'ENVIRONMENTAL_PILLAR_WEIGHT', 'ENVIRONMENTAL_PILLAR_QUARTILE',
        'CLIMATE_CHANGE_THEME_SCORE', 'CLIMATE_CHANGE_THEME_WEIGHT', 'ENVIRONMENTAL_OPPS_THEME_SCORE',
        'ENVIRONMENTAL_OPPS_THEME_WEIGHT', 'NATURAL_RES_USE_THEME_SCORE', 'NATURAL_RES_USE_THEME_WEIGHT',
        'WASTE_MGMT_THEME_SCORE', 'WASTE_MGMT_THEME_WEIGHT', 'E_WASTE_WEIGHT', 'FINANCING_ENV_IMP_WEIGHT',
        'OPPS_CLN_TECH_SCORE', 'OPPS_CLN_TECH_QUARTILE', 'OPPS_CLN_TECH_WEIGHT', 'OPPS_GREEN_BUILDING_WEIGHT',
        'OPPS_RENEW_ENERGY_WEIGHT', 'PACK_MAT_WASTE_WEIGHT', 'PROD_CARB_FTPRNT_SCORE', 'PROD_CARB_FTPRNT_QUARTILE',
        'PROD_CARB_FTPRNT_WEIGHT', 'RAW_MAT_SRC_WEIGHT', 'TOXIC_EMISS_WSTE_SCORE', 'TOXIC_EMISS_WASTE_QUARTILE',
        'TOXIC_EMISS_WSTE_WEIGHT', 'WATER_STRESS_SCORE', 'WATER_STRESS_QUARTILE', 'WATER_STRESS_WEIGHT',
        'BIODIV_LAND_USE_SCORE', 'BIODIV_LAND_USE_WEIGHT', 'CARBON_EMISSIONS_SCORE', 'CARBON_EMISSIONS_WEIGHT',
        'INS_CLIMATE_CHG_RISK_WEIGHT'
    ]

    social_features = [
        'SOCIAL_PILLAR_SCORE', 'SOCIAL_PILLAR_WEIGHT', 'SOCIAL_PILLAR_QUARTILE', 'HUMAN_CAPITAL_THEME_SCORE',
        'HUMAN_CAPITAL_THEME_WEIGHT', 'PRODUCT_SAFETY_THEME_SCORE', 'PRODUCT_SAFETY_THEME_WEIGHT',
        'SOCIAL_OPPS_THEME_SCORE', 'SOCIAL_OPPS_THEME_WEIGHT', 'STAKEHOLDER_OPPOSIT_THEME_SCORE',
        'STAKEHOLDER_OPPOSIT_THEME_WEIGHT', 'ACCESS_TO_COMM_WEIGHT', 'ACCESS_TO_FIN_WEIGHT', 'ACCESS_TO_HLTHCRE_WEIGHT',
        'CHEM_SAFETY_SCORE', 'CHEM_SAFETY_QUARTILE', 'CHEM_SAFETY_WEIGHT', 'COMM_REL_WEIGHT', 'FIN_PROD_SAFETY_WEIGHT',
        'CONTROV_SRC_WEIGHT', 'HLTH_SAFETY_SCORE', 'HLTH_SAFETY_QUARTILE', 'INS_HLTH_DEMO_RISK_WEIGHT',
        'HLTH_SAFETY_WEIGHT', 'HUMAN_CAPITAL_DEV_SCORE', 'HUMAN_CAPITAL_DEV_QUARTILE', 'HUMAN_CAPITAL_DEV_WEIGHT',
        'LABOR_MGMT_SCORE', 'LABOR_MGMT_QUARTILE', 'LABOR_MGMT_WEIGHT', 'OPPS_NUTRI_HLTH_WEIGHT',
        'PRIVACY_DATA_SEC_SCORE', 'PRIVACY_DATA_SEC_QUARTILE', 'PRIVACY_DATA_SEC_WEIGHT', 'PROD_SFTY_QUALITY_SCORE',
        'PROD_SFTY_QUALITY_QUARTILE', 'PROD_SFTY_QUALITY_WEIGHT', 'RESPONSIBLE_INVEST_WEIGHT', 'SUPPLY_CHAIN_LAB_WEIGHT'
    ]

    governance_features = [
        'GOVERNANCE_PILLAR_SCORE', 'GOVERNANCE_PILLAR_WEIGHT', 'GOVERNANCE_PILLAR_QUARTILE', 'BUSINESS_ETHICS_THEME_SCORE',
        'CORPORATE_GOV_THEME_SCORE', 'ACCOUNTING_SCORE', 'BOARD_SCORE', 'CORP_GOVERNANCE_SCORE', 'CORP_GOVERNANCE_QUARTILE',
        'OWNERSHIP_AND_CONTROL_SCORE', 'PAY_SCORE', 'BUS_ETHICS_GOV_PILLAR_SD', 'BUS_ETHICS_PCTL_GLOBAL',
        'BUS_ETHICS_PCTL_HOME', 'CORP_BEHAV_ETHICS_SCORE', 'CORP_BEHAV_GOV_PILLAR_SD', 'CORP_BEHAV_PCTL_GLOBAL',
        'CORP_BEHAV_PCTL_HOME', 'TAX_TRANSP_GOV_PILLAR_SD', 'TAX_TRANSP_PCTL_GLOBAL', 'TAX_TRANSP_PCTL_HOME',
        'ACCOUNTING_GOV_PILLAR_SD', 'ACCOUNTING_PCTL_GLOBAL', 'ACCOUNTING_PCTL_HOME', 'BOARD_GOV_PILLAR_SD',
        'BOARD_PCTL_GLOBAL', 'BOARD_PCTL_HOME', 'CORP_GOVERNANCE_GOV_PILLAR_SD', 'GOVERNANCE_PCTL_GLOBAL',
        'GOVERNANCE_PCTL_HOME', 'OWNERSHIP_GOV_PILLAR_SD', 'OWNERSHIP_PCTL_GLOBAL', 'OWNERSHIP_PCTL_HOME',
        'PAY_GOV_PILLAR_SD', 'PAY_PCTL_GLOBAL', 'PAY_PCTL_HOME', 'CORP_BEHAV_SCORE', 'CORP_BEHAV_QUARTILE',
        'CORP_BEHAV_TAX_TRANSP_SCORE'
    ]

    # Create dropdowns for each gauge
    col4, col5, col6 = st.columns(3)

    with col4:
        selected_env_feature = st.selectbox('Select Environmental Feature', environmental_features)
        env_value = company_data[selected_env_feature].values[0] if selected_env_feature in company_data else None
        env_color = "darkgray" if env_value is None else "darkblue"
        env_value = 0 if env_value is None else env_value
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=env_value,
            title={'text': selected_env_feature.replace('_', ' ').title()},
            gauge={
                'axis': {'range': [0, 10]},
                'bar': {'color': env_color},
                'steps': [
                    {'range': [0, 2.5], 'color': "red"},
                    {'range': [2.5, 5], 'color': "orange"},
                    {'range': [5, 7.5], 'color': "yellow"},
                    {'range': [7.5, 10], 'color': "green"}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 4},
                    'thickness': 0.75,
                    'value': env_value
                }
            }
        ))
        st.plotly_chart(fig)

    with col5:
        selected_soc_feature = st.selectbox('Select Social Feature', social_features)
        soc_value = company_data[selected_soc_feature].values[0] if selected_soc_feature in company_data else None
        soc_color = "darkgray" if soc_value is None else "darkblue"
        soc_value = 0 if soc_value is None else soc_value
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=soc_value,
            title={'text': selected_soc_feature.replace('_', ' ').title()},
            gauge={
                'axis': {'range': [0, 10]},
                'bar': {'color': soc_color},
                'steps': [
                    {'range': [0, 2.5], 'color': "red"},
                    {'range': [2.5, 5], 'color': "orange"},
                    {'range': [5, 7.5], 'color': "yellow"},
                    {'range': [7.5, 10], 'color': "green"}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 4},
                    'thickness': 0.75,
                    'value': soc_value
                }
            }
        ))
        st.plotly_chart(fig)

    with col6:
        selected_gov_feature = st.selectbox('Select Governance Feature', governance_features)
        gov_value = company_data[selected_gov_feature].values[0] if selected_gov_feature in company_data else None
        gov_color = "darkgray" if gov_value is None else "darkblue"
        gov_value = 0 if gov_value is None else gov_value
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=gov_value,
            title={'text': selected_gov_feature.replace('_', ' ').title()},
            gauge={
                'axis': {'range': [0, 10]},
                'bar': {'color': gov_color},
                'steps': [
                    {'range': [0, 2.5], 'color': "red"},
                    {'range': [2.5, 5], 'color': "orange"},
                    {'range': [5, 7.5], 'color': "yellow"},
                    {'range': [7.5, 10], 'color': "green"}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 4},
                    'thickness': 0.75,
                    'value': gov_value
                }
            }
        ))
        st.plotly_chart(fig)



    # 5. Risk and Opportunity Score as Gauge Plot
    # Arrange plots in a grid layout
    # col4, col5, col6 = st.columns(3)
    # fig = go.Figure(go.Indicator(
    #     mode="gauge+number",
    #     value=company_data['WATER_STRESS_SCORE'].values[0],
    #     title={'text': "Water Stress Score"},
    #     gauge={
    #         'axis': {'range': [0, 10]},
    #         'bar': {'color': "darkblue"},
    #         'steps': [
    #             {'range': [0, 2.5], 'color': "red"},
    #             {'range': [2.5, 5], 'color': "orange"},
    #             {'range': [5, 7.5], 'color': "yellow"},
    #             {'range': [7.5, 10], 'color': "green"}
    #         ],
    #         'threshold': {
    #             'line': {'color': "black", 'width': 4},
    #             'thickness': 0.75,
    #             'value': company_data['WATER_STRESS_SCORE'].values[0]
    #         }
    #     }
    # ))
    # with col4:
    #     st.plotly_chart(fig)

    # fig = go.Figure(go.Indicator(
    #     mode="gauge+number",
    #     value=company_data['TOXIC_EMISS_WSTE_SCORE'].values[0],
    #     title={'text': "Toxic Emissions and Waste Score"},
    #     gauge={
    #         'axis': {'range': [0, 10]},
    #         'bar': {'color': "darkblue"},
    #         'steps': [
    #             {'range': [0, 2.5], 'color': "red"},
    #             {'range': [2.5, 5], 'color': "orange"},
    #             {'range': [5, 7.5], 'color': "yellow"},
    #             {'range': [7.5, 10], 'color': "green"}
    #         ],
    #         'threshold': {
    #             'line': {'color': "black", 'width': 4},
    #             'thickness': 0.75,
    #             'value': company_data['WATER_STRESS_SCORE'].values[0]
    #         }
    #     }
    # ))
    # with col5:
    #     st.plotly_chart(fig)

    # fig = go.Figure(go.Indicator(
    #     mode="gauge+number",
    #     value=company_data['ACCOUNTING_SCORE'].values[0],
    #     title={'text': "Accounting Score"},
    #     gauge={
    #         'axis': {'range': [0, 10]},
    #         'bar': {'color': "darkblue"},
    #         'steps': [
    #             {'range': [0, 2.5], 'color': "red"},
    #             {'range': [2.5, 5], 'color': "orange"},
    #             {'range': [5, 7.5], 'color': "yellow"},
    #             {'range': [7.5, 10], 'color': "green"}
    #         ],
    #         'threshold': {
    #             'line': {'color': "black", 'width': 4},
    #             'thickness': 0.75,
    #             'value': company_data['WATER_STRESS_SCORE'].values[0]
    #         }
    #     }
    # ))
    # with col6:
    #     st.plotly_chart(fig)    
    

    # TEST
    # Calculate average ESG scores per industry
    # esg_scores = df.groupby('IVA_INDUSTRY')[['ENVIRONMENTAL_PILLAR_SCORE', 'SOCIAL_PILLAR_SCORE', 'GOVERNANCE_PILLAR_SCORE']].mean()

    # # Plot the stacked bar chart
    # esg_scores.plot(kind='bar', stacked=True)
    # with col6:
    #     st.pyplot(plt)