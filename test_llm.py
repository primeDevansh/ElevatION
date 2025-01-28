import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from gpt4all import GPT4All
# import os

# from call_llama import call_llm

import google.generativeai as genai
genai.configure(api_key="AIzaSyDMsQijYv_8F31Q0AqM12lPKU7AUDbIjW4")
model = genai.GenerativeModel("gemini-1.5-flash")

# os.environ['SSL_CERT_FILE'] = './certificates/ca-bundle.pem'
# os.environ['REQUESTS_CA_BUNDLE'] = './certificates/ca-bundle.pem'

pageName = 'Company ESGically'
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
st.write("Deep dive into the ESG scores of a particular company here!")
# Sidebar logo
st.logo('Assets/LogoWithoutBG.webp')

# START
cleanedSampleDataPath = 'sampleData/sample_with_names.csv'

# Load your dataset
df = pd.read_csv(cleanedSampleDataPath)

# Dropdown to select a company
company_options = ['None'] + list(df['CompanyName'].unique())
company = st.selectbox('Select Company', company_options)

# Filter data for the selected company
company_data = df[df['CompanyName'] == company]

# Display detailed report if data is not empty
if not company_data.empty:
    st.write(f"### Detailed Report for {company}")

    col1, col2 = st.columns(2)

    # Bar Chart for Average Scores
    avg_scores = company_data[['ENVIRONMENTAL_PILLAR_SCORE', 'SOCIAL_PILLAR_SCORE', 'GOVERNANCE_PILLAR_SCORE']].mean().reset_index()
    avg_scores.columns = ['Metric', 'Average Score']
    fig_bar = px.bar(avg_scores, x='Metric', y='Average Score', title='Average Scores',
                    template='plotly_dark',  # Modern look
                    color='Metric',
                    color_discrete_sequence=px.colors.qualitative.Vivid)
    col1.plotly_chart(fig_bar, use_container_width=True)
    
    # Display ESG scores
    with col2:
        # 1. IVA Company Rating
        rating = company_data['IVA_COMPANY_RATING'].values[0]

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
            <div style='background-color: {color}; padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 20px;'>
                <strong style='font-size: 18px;'>Company ESG Score: {rating}</strong>
            </div>
            """, unsafe_allow_html=True)

        st.write(" ")
        # Display company information
        st.write("#### Company Information")
        st.write(company_data[['CompanyName', 'IVA_INDUSTRY', 'GICS_SUB_IND']].drop_duplicates())

        st.write("#### ESG Scores")
        esg_scores = company_data[['ENVIRONMENTAL_PILLAR_SCORE', 'SOCIAL_PILLAR_SCORE', 'GOVERNANCE_PILLAR_SCORE']].mean()
        st.write(esg_scores)
    
    # Display metrics grouped into E, S, and G categories
    e_metrics = {
        "Environmental Pillar Score": company_data['ENVIRONMENTAL_PILLAR_SCORE'].mean(),
        "Climate Change Theme Score": company_data['CLIMATE_CHANGE_THEME_SCORE'].mean(),
        "Carbon Footprint Score": company_data['PROD_CARB_FTPRNT_SCORE'].mean(),
        "Natural Resource Use Theme Score": company_data['NATURAL_RES_USE_THEME_SCORE'].mean(),
        "Carbon Emissions Score": company_data['CARBON_EMISSIONS_SCORE'].mean(),
        "Biodiversity Land Use Score": company_data['BIODIV_LAND_USE_SCORE'].mean(),
        "Waste Management Theme Score": company_data['WASTE_MGMT_THEME_SCORE'].mean(),
        "Toxic Emissions and Waste Score": company_data['TOXIC_EMISS_WSTE_SCORE'].mean(),
        "Water Stress Score": company_data['WATER_STRESS_SCORE'].mean()
    }
    
    s_metrics = {
        "Social Pillar Score": company_data['SOCIAL_PILLAR_SCORE'].mean(),
        "Business Ethics Theme Score": company_data['BUSINESS_ETHICS_THEME_SCORE'].mean(),
        "Human Capital Theme Score": company_data['HUMAN_CAPITAL_THEME_SCORE'].mean(),
        "Privacy Data Security Score": company_data['PRIVACY_DATA_SEC_SCORE'].mean(),
        "Chemical Safety Score": company_data['CHEM_SAFETY_SCORE'].mean(),
        "Health Safety Score": company_data['HLTH_SAFETY_SCORE'].mean(),
        "Labor Management Score": company_data['LABOR_MGMT_SCORE'].mean(),
        "Stakeholder Opposition Score": company_data['STAKEHOLDER_OPPOSIT_THEME_SCORE'].mean(),
        "Responsible Investment Score": company_data['RESPONSIBLE_INVEST_SCORE'].mean()
    }
    
    g_metrics = {
        "Governance Pillar Score": company_data['GOVERNANCE_PILLAR_SCORE'].mean(),
        "Corporate Behavior Score": company_data['CORP_BEHAV_SCORE'].mean(),
        "Board Score": company_data['BOARD_SCORE'].mean(),
        "Pay Score": company_data['PAY_SCORE'].mean(),
        "Tax Transparency Score": company_data['TAX_TRANSP_GOV_PILLAR_SD'].mean(),
        "Product Safety Theme Score": company_data['PRODUCT_SAFETY_THEME_SCORE'].mean(),
        "Board Governance Score": company_data['BOARD_GOV_PILLAR_SD'].mean(),
        "Ownership and Control Score": company_data['OWNERSHIP_AND_CONTROL_SCORE'].mean(),
        "Pay Governance Score": company_data['PAY_GOV_PILLAR_SD'].mean()
    }
    
    # Display metrics in columns with color coding and spacing
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("### Environmental Metrics")
        for metric, value in e_metrics.items():
            if pd.isna(value):
                color = '#4B4B4B'  # Darker gray for NaN values
                metric_display = f"<s>{metric}</s>"
                value_display = "Data not available"
            elif value >= 7:
                color = '#166352'  # Green
                metric_display = metric
                value_display = f"{value:.2f}/10"
            elif 4 <= value < 7:
                color = '#FBA600'  # Yellow
                metric_display = metric
                value_display = f"{value:.2f}/10"
            else:
                color = '#BD1C2B'  # Red
                metric_display = metric
                value_display = f"{value:.2f}/10"
            st.markdown(f"""
                <div style='background-color: {color}; padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 20px;'>
                    <strong style='font-size: 18px;'>{metric_display}</strong><br>
                    <strong style='font-size: 20px;'>{value_display}</strong>
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        st.write("### Social Metrics")
        for metric, value in s_metrics.items():
            if pd.isna(value):
                color = '#4B4B4B'  # Darker gray for NaN values
                metric_display = f"<s>{metric}</s>"
                value_display = "Data not available"
            elif value >= 7:
                color = '#166352'  # Green
                metric_display = metric
                value_display = f"{value:.2f}/10"
            elif 4 <= value < 7:
                color = '#FBA600'  # Yellow
                metric_display = metric
                value_display = f"{value:.2f}/10"
            else:
                color = '#BD1C2B'  # Red
                metric_display = metric
                value_display = f"{value:.2f}/10"
            st.markdown(f"""
		    <div style='background-color: {color}; padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 20px;'>
                    <strong style='font-size: 18px;'>{metric_display}</strong><br>
                    <strong style='font-size: 20px;'>{value_display}</strong>
                </div>
                """, unsafe_allow_html=True)

    with col3:
        st.write("### Governance Metrics")
        for metric, value in g_metrics.items():
            if pd.isna(value):
                color = '#4B4B4B'  # Darker gray for NaN values
                metric_display = f"<s>{metric}</s>"
                value_display = "Data not available"
            elif value >= 7:
                color = '#166352'  # Green
                metric_display = metric
                value_display = f"{value:.2f}/10"
            elif 4 <= value < 7:
                color = '#FBA600'  # Yellow
                metric_display = metric
                value_display = f"{value:.2f}/10"
            else:
                color = '#BD1C2B'  # Red
                metric_display = metric
                value_display = f"{value:.2f}/10"
            st.markdown(f"""
                <div style='background-color: {color}; padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 20px;'>
                    <strong style='font-size: 18px;'>{metric_display}</strong><br>
                    <strong style='font-size: 20px;'>{value_display}</strong>
                </div>
                """, unsafe_allow_html=True)

    # Summarize ESG data
    esg_text = f"""
    Company: {company}
    Industry: {company_data['IVA_INDUSTRY'].values[0]}
    Sub-Industry: {company_data['GICS_SUB_IND'].values[0]}
    Environmental Pillar Score: {e_metrics['Environmental Pillar Score']}
    Climate Change Theme Score: {e_metrics['Climate Change Theme Score']}
    Carbon Footprint Score: {e_metrics['Carbon Footprint Score']}
    Natural Resource Use Theme Score: {e_metrics['Natural Resource Use Theme Score']}
    Carbon Emissions Score: {e_metrics['Carbon Emissions Score']}
    Biodiversity Land Use Score: {e_metrics['Biodiversity Land Use Score']}
    Waste Management Theme Score: {e_metrics['Waste Management Theme Score']}
    Toxic Emissions and Waste Score: {e_metrics['Toxic Emissions and Waste Score']}
    Water Stress Score: {e_metrics['Water Stress Score']}
    Social Pillar Score: {s_metrics['Social Pillar Score']}
    Business Ethics Theme Score: {s_metrics['Business Ethics Theme Score']}
    Human Capital Theme Score: {s_metrics['Human Capital Theme Score']}
    Privacy Data Security Score: {s_metrics['Privacy Data Security Score']}
    Chemical Safety Score: {s_metrics['Chemical Safety Score']}
    Health Safety Score: {s_metrics['Health Safety Score']}
    Labor Management Score: {s_metrics['Labor Management Score']}
    Stakeholder Opposition Score: {s_metrics['Stakeholder Opposition Score']}
    Responsible Investment Score: {s_metrics['Responsible Investment Score']}
    Governance Pillar Score: {g_metrics['Governance Pillar Score']}
    Corporate Behavior Score: {g_metrics['Corporate Behavior Score']}
    Board Score: {g_metrics['Board Score']}
    Pay Score: {g_metrics['Pay Score']}
    Tax Transparency Score: {g_metrics['Tax Transparency Score']}
    Product Safety Theme Score: {g_metrics['Product Safety Theme Score']}
    Board Governance Score: {g_metrics['Board Governance Score']}
    Ownership and Control Score: {g_metrics['Ownership and Control Score']}
    Pay Governance Score: {g_metrics['Pay Governance Score']}
    """

    if st.button('Generate Summary'):
        # system_message = {"role": "system", "content": "You are an intelligent assistant, trained to generate summaries in natural language based on the provided data. Return a summary of maximum 100 words."}
        # user_message = {"role": "user", "content": f"These are the values you shoul consider: {esg_text}"}
        # messages = [system_message, user_message]
        # sector = call_llm(messages)
        # st.write(sector)

        response = model.generate_content("Explain how AI works")
        st.write(response)

        # summary = model.summarize(esg_text)
        # st.write("### Summary")
        # st.write(summary)

else:
    st.write("Please select a company to view the detailed report.")


