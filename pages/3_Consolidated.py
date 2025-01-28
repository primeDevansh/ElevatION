import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

pageName = 'Consolidated Industry Scores'
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
st.logo('Assets/LogoWithoutBG.webp')

# START

cleanedSampleDataPath = 'sampleData/sample_with_names.csv'

# Load your dataset
df = pd.read_csv(cleanedSampleDataPath)

# Dropdowns to select industry and sub-industry
industry_options = ['None'] + list(df['IVA_INDUSTRY'].unique())
industry = st.selectbox('Select Industry', industry_options)
sub_industry_options = ['None'] + list(df[df['IVA_INDUSTRY'] == industry]['GICS_SUB_IND'].unique()) if industry != 'None' else ['None']
sub_industry = st.selectbox('Select Sub-Industry', sub_industry_options)

# Filter data for the selected industry and sub-industry
if industry != 'None':
    industry_data = df[df['IVA_INDUSTRY'] == industry]
    if sub_industry != 'None':
        data = industry_data[industry_data['GICS_SUB_IND'] == sub_industry]
    else:
        data = industry_data
else:
    data = pd.DataFrame()  # Empty DataFrame when no industry is selected

# Function to calculate mode
def calculate_mode(series):
    return series.mode()[0] if not series.mode().empty else None

# Display consolidated report if data is not empty
if not data.empty:
    report_title = f"Consolidated Report for {'Sub-Industry: ' + sub_industry if sub_industry != 'None' else 'Industry: ' + industry}"
    st.write(f"### {report_title}")
    
    # 1. Mode of IVA Company Rating
    rating = calculate_mode(data['IVA_COMPANY_RATING'])

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
            <strong style='font-size: 16px;'>Mode of IVA Company Rating: {rating}</strong>
        </div>
        """, unsafe_allow_html=True)

    st.write(" ")

    # Modern Graph for IVA Company Ratings
    # Define a ranking for the ratings to ensure proper ordering and visibility
    rating_rank = {'AAA': 7, 'AA': 6, 'A': 5, 'BBB': 4, 'BB': 3, 'B': 2, 'CCC': 1}
    data['Rating Rank'] = data['IVA_COMPANY_RATING'].map(rating_rank)

    fig = px.bar(data.sort_values('Rating Rank'), x='ISSUERID', y='Rating Rank', color='IVA_COMPANY_RATING',
                 color_discrete_map={
                     'AAA': '#166352',
                     'AA': '#166352',
                     'A': '#FBA600',
                     'BBB': '#FBA600',
                     'BB': '#FBA600',
                     'B': '#BD1C2B',
                     'CCC': '#BD1C2B'
                 },
                 title='IVA Company Ratings for Selected Industry and Sub-Industry')
    
    # Update layout to make bars thin and ensure all ratings are displayed
    fig.update_traces(marker_line_width=0.5, marker_line_color='black', width=0.5)
    fig.update_layout(bargap=0.1, xaxis_tickangle=-45)
    
    st.plotly_chart(fig, use_container_width=True)

    # Display metrics grouped into E, S, and G categories
    e_metrics = {
        "Average Environmental Pillar Score": data['ENVIRONMENTAL_PILLAR_SCORE'].mean(),
        "Average Climate Change Theme Score": data['CLIMATE_CHANGE_THEME_SCORE'].mean(),
        "Average Carbon Footprint Score": data['PROD_CARB_FTPRNT_SCORE'].mean(),
        "Average Natural Resource Use Theme Score": data['NATURAL_RES_USE_THEME_SCORE'].mean(),
        "Average Carbon Emissions Score": data['CARBON_EMISSIONS_SCORE'].mean(),
        "Average Biodiversity Land Use Score": data['BIODIV_LAND_USE_SCORE'].mean(),
        "Average Waste Management Theme Score": data['WASTE_MGMT_THEME_SCORE'].mean(),
        "Average Toxic Emissions and Waste Score": data['TOXIC_EMISS_WSTE_SCORE'].mean(),
        "Average Water Stress Score": data['WATER_STRESS_SCORE'].mean()
    }
    
    s_metrics = {
        "Average Social Pillar Score": data['SOCIAL_PILLAR_SCORE'].mean(),
        "Average Business Ethics Theme Score": data['BUSINESS_ETHICS_THEME_SCORE'].mean(),
        "Average Human Capital Theme Score": data['HUMAN_CAPITAL_THEME_SCORE'].mean(),
        "Average Privacy Data Security Score": data['PRIVACY_DATA_SEC_SCORE'].mean(),
        "Average Chemical Safety Score": data['CHEM_SAFETY_SCORE'].mean(),
        "Average Health Safety Score": data['HLTH_SAFETY_SCORE'].mean(),
        "Average Labor Management Score": data['LABOR_MGMT_SCORE'].mean(),
        "Average Stakeholder Opposition Score": data['STAKEHOLDER_OPPOSIT_THEME_SCORE'].mean(),
        "Average Responsible Investment Score": data['RESPONSIBLE_INVEST_WEIGHT'].mean()
    }
    
    g_metrics = {
        "Average Governance Pillar Score": data['GOVERNANCE_PILLAR_SCORE'].mean(),
        "Average Corporate Behavior Score": data['CORP_BEHAV_SCORE'].mean(),
        "Average Board Score": data['BOARD_SCORE'].mean(),
        "Average Pay Score": data['PAY_SCORE'].mean(),
        "Average Tax Transparency Score": data['TAX_TRANSP_GOV_PILLAR_SD'].mean(),
        "Average Product Safety Theme Score": data['PRODUCT_SAFETY_THEME_SCORE'].mean(),
        # "Average Accounting Score": data['ACCOUNTING_SCORE'].mean(),
        "Average Board Governance Score": data['BOARD_GOV_PILLAR_SD'].mean(),
        "Average Ownership and Control Score": data['OWNERSHIP_AND_CONTROL_SCORE'].mean(),
        "Average Pay Governance Score": data['PAY_GOV_PILLAR_SD'].mean()
    }
    
    # Display metrics in columns with color coding and spacing
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("### Environmental Metrics")
        for metric, value in e_metrics.items():
            if value >= 7:
                color = '#166352'  # Green
            elif 4 <= value < 7:
                color = '#FBA600'  # Yellow
            else:
                color = '#BD1C2B'  # Red
            st.markdown(f"""
                <div style='background-color: {color}; padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 20px;'>
                    <strong style='font-size: 14px;'>{metric}</strong><br>
                    <strong style='font-size: 16px;'>{value:.2f}/10</strong>
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        st.write("### Social Metrics")
        for metric, value in s_metrics.items():
            if value >= 7:
                color = '#166352'  # Green
            elif 4 <= value < 7:
                color = '#FBA600'  # Yellow
            else:
                color = '#BD1C2B'  # Red
            st.markdown(f"""
                <div style='background-color: {color}; padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 20px;'>
                    <strong style='font-size: 14px;'>{metric}</strong><br>
                    <strong style='font-size: 16px;'>{value:.2f}/10</strong>
                </div>
                """, unsafe_allow_html=True)
    
    with col3:
        st.write("### Governance Metrics")
        for metric, value in g_metrics.items():
            if value >= 7:
                color = '#166352'  # Green
            elif 4 <= value < 7:
                color = '#FBA600'  # Yellow
            else:
                color = '#BD1C2B'  # Red
            st.markdown(f"""
                <div style='background-color: {color}; padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 20px;'>
                    <strong style='font-size: 14px;'>{metric}</strong><br>
                    <strong style='font-size: 16px;'>{value:.2f}/10</strong>
                </div>
                """, unsafe_allow_html=True)
    
    # Modern Graphs

    col1, col2 = st.columns(2)

    # Bar Chart for Average Scores
    avg_scores = data[['INDUSTRY_ADJUSTED_SCORE', 'WEIGHTED_AVERAGE_SCORE']].mean().reset_index()
    avg_scores.columns = ['Metric', 'Average Score']
    fig_bar = px.bar(avg_scores, x='Metric', y='Average Score', title='Average Scores',
                    template='plotly_dark',  # Modern look
                    color='Metric',
                    color_discrete_sequence=px.colors.qualitative.Vivid)
    col1.plotly_chart(fig_bar, use_container_width=True)

    # Pie Chart for Distribution of Ratings
    rating_counts = data['IVA_COMPANY_RATING'].value_counts().reset_index()
    rating_counts.columns = ['Rating', 'Count']

    # Define color scheme for the ratings
    color_scheme = {
        'AAA': '#166352',
        'AA': '#166352',
        'A': '#FBA600',
        'BBB': '#FBA600',
        'BB': '#FBA600',
        'B': '#BD1C2B',
        'CCC': '#BD1C2B'
    }

    fig_pie = px.pie(rating_counts, values='Count', names='Rating', title='Distribution of IVA Company Ratings',
                    color='Rating',
                    color_discrete_map=color_scheme)
    col2.plotly_chart(fig_pie, use_container_width=True)
else:
    st.write("Please select an industry to view the consolidated report.")