import warnings
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import AsIs
import seaborn as sns
import streamlit as st

warnings.filterwarnings('ignore')

def load_data_from_postgres(start_date, end_date):
    conn = psycopg2.connect(
        dbname='action-learning',
        user='postgres',
        password='sup3r',
        host='localhost',
        port='5432'
    )
    cursor = conn.cursor()
    
    query = sql.SQL("""
        SELECT * FROM data_problem_stats
        WHERE "error_time_found" >= %s AND "error_time_found" <= %s
    """)
    cursor.execute(query, (start_date, end_date))
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()
    df = pd.DataFrame(data, columns=columns)
    return df

st.title("Data Quality Dashboard")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

@st.cache 
def load_data(file):
    data = pd.read_csv(file)
    return data

uploaded_file = st.sidebar.file_uploader("Please choose a file")

if uploaded_file is None:
    st.warning("No file uploaded. Using data from PostgreSQL.", icon="ℹ️")
    start_date = "2022-01-01"
    end_date = "2024-12-31"
    
    # Load data from PostgreSQL
    df = load_data_from_postgres(start_date, end_date)
    
else:
    df = load_data(uploaded_file)

# Sidebar for filters
st.sidebar.title("Data Quality Dashboard Filters")

# Filter by Error Time
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2022-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2024-12-31"))

# Filter data based on selected criteria
filtered_data = df[(df['error_time_found'] >= start_date) & (df['error_time_found'] <= end_date)]

# i. Number of Detected Issues
st.header("Number of Detected Issues")
st.write(f"Total Detected Issues: {len(filtered_data)}")

# ii. Proportion of Problems (Pie Chart)
st.header("Proportion of Problems")
problem_counts = filtered_data['expectation_type'].value_counts()
fig_pie = px.pie(problem_counts, names=problem_counts.index, title="Proportion of Problems")
st.plotly_chart(fig_pie)

# iii. Data Problem Stats Table
st.header("Data Problem Stats Table")
st.dataframe(filtered_data[['id', 'file_name', 'column', 'expectation_type', 'unexpected_values', 'error_time_found']])

st.write("This is the Data Quality dashboard.")
