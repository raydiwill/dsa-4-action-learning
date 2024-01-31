import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import psycopg2
from psycopg2 import sql

def main():
    st.header("Customer Profile")

# Connect to PostgreSQL
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
        SELECT * FROM customers_model
        WHERE "pred_date" >= %s AND "pred_date" <= %s LIMIT 1000
    """)
    cursor.execute(query, (start_date, end_date))
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()
    df = pd.DataFrame(data, columns=columns)
    return df

# Load data from file or PostgreSQL
uploaded_file = st.sidebar.file_uploader("Please choose a file")
if uploaded_file is None:
    st.warning("No file uploaded. Using data from PostgreSQL.", icon="ℹ️")
    start_date = "2022-01-01"
    end_date = "2024-12-31"
    df = load_data_from_postgres(start_date, end_date)
else:
    df = pd.read_csv(uploaded_file)

# Filter data based on user input
churn_options = ["All", "Churn", "No Churn"]
risk_options = ["All", "High Risk", "Low Risk"]

churn_filter = st.sidebar.selectbox("Churn/No Churn", churn_options, index=0)
risk_filter = st.sidebar.selectbox("High/Low Risk", risk_options, index=0)

if "pred_date" in df.columns:
    df["pred_date"] = pd.to_datetime(df["pred_date"], errors="coerce")

    # Apply filters
    if churn_filter == "Churn":
        df = df[df["pred_churn"] == True]  
    elif churn_filter == "No Churn":
        df = df[df["pred_churn"] == False]  

    if risk_filter == "High Risk":
        df = df[df["pred_risk"] == "High"]
    elif risk_filter == "Low Risk":
        df = df[df["pred_risk"] == "Low"]

# Fill missing values
numeric_columns = ['REVENUE', 'ARPU_SEGMENT', 'FREQUENCE', 'DATA_VOLUME', 'ON_NET', 'ORANGE', 'TIGO', 'REGULARITY', 'FREQ_TOP_PACK']
df[numeric_columns] = df[numeric_columns].fillna(0)

# Create subplots
num_plots = len(numeric_columns)
fig = make_subplots(rows=num_plots, cols=2, subplot_titles=[f"{col} by pred_date" for col in numeric_columns],
                    shared_xaxes=True, vertical_spacing=0.1)

# Plot numeric columns against time and region
for i, column in enumerate(numeric_columns, start=1):
    # Line plot against time
    trace1 = go.Scatter(x=df["pred_date"], y=df[column], mode='lines+markers', name='By Time')
    
    # Box plot against region
    trace2 = go.Box(x=df["REGION"], y=df[column], name='By REGION')
    
    # Add traces to subplots
    fig.add_trace(trace1, row=i, col=1)
    fig.add_trace(trace2, row=i, col=2)

# Update layout
fig.update_layout(height=num_plots * 300, showlegend=False, title_text="Numeric Columns Trends Over Time and Region")
st.plotly_chart(fig)

if __name__ == "__main__":
    main()