# Markdown is supported

import streamlit as st

st.write("Hello world!")
name = st.text_input("Enter your name: ")

st.write(f"Your name is {name}")

is_clicked = st.button("Bang me!")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv(".\sampleData\cleaned_sample_data.csv")
st.write(data)

industries = data['IVA_INDUSTRY'].unique()
selected_industry = st.selectbox("Select an industry", industries)
filtered_data = data[data['IVA_INDUSTRY'] == selected_industry]

st.write("Select columns to plot")
columns = st.multiselect("Columns", filtered_data.columns)

if columns:
    st.write("Plotting data...")
    fig, ax = plt.subplots()
    filtered_data[columns].plot(ax=ax)
    st.pyplot(fig)