import streamlit as st
import importlib

# Set page config
st.set_page_config(page_title='My Multi-Page App', page_icon=':books:', layout='wide')

# Add your dashboard scripts here
dashboard_scripts = [
    "Analyzed_Predictions",
    "Customer_Profile",
    "Data_Quality",
    "Monitoring_Dashboard"
]

# Sidebar to select dashboard
selected_dashboard = st.sidebar.selectbox("Select Dashboard", dashboard_scripts)

# Import and run the selected dashboard
dashboard_module = importlib.import_module(selected_dashboard)
dashboard_module.run()
