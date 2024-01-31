import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns
from sklearn.metrics import precision_recall_curve, confusion_matrix, classification_report, roc_curve, auc
import matplotlib.pyplot as plt
import plotly.express as px
import os
import warnings
import numpy as np
from plotly.subplots import make_subplots
import psycopg2
from psycopg2 import sql

warnings.filterwarnings('ignore')

def run():
    def main():
        st.header("Analyzed Predictions")

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

    # Set Streamlit page configuration
    # st.set_page_config(
        page_title=":chart_with_upwards_trend: Analyzed Returned Predictions Dashboard",
        page_icon=":bar_chart:",
        layout="wide" 
        
        # Load data from file or PostgreSQL
    uploaded_file = st.sidebar.file_uploader("Please choose a file")
    if uploaded_file is None:
        st.warning("No file uploaded. Using data from PostgreSQL.", icon="ℹ️")
        start_date = "2022-01-01"
        end_date = "2024-12-31"
        df = load_data_from_postgres(start_date, end_date)
    else:
        df = pd.read_csv(uploaded_file)

    # Sidebar filters
    churn_options = ["All", "Churn", "No Churn"]
    risk_options = ["All", "High Risk", "Low Risk"]
    churn_filter = st.sidebar.selectbox("Churn/No Churn", churn_options, index=0)
    risk_filter = st.sidebar.selectbox("High/Low Risk", risk_options, index=0)

    # Apply filters
    if "pred_date" in df.columns:
        df["pred_date"] = pd.to_datetime(df["pred_date"], errors="coerce")

        if churn_filter == "Churn":
            df = df[df["pred_churn"] == True]  
        elif churn_filter == "No Churn":
            df = df[df["pred_churn"] == False]  

        if risk_filter == "High Risk":
            df = df[df["pred_risk"] == "High"]
        elif risk_filter == "Low Risk":
            df = df[df["pred_risk"] == "Low"]

    # Check if dataframe is empty
    if df.empty:
        st.warning("No data available for the selected filters.")
    else:
        # Display the dataframe
        with st.expander("Data Preview", expanded=True):
            st.dataframe(
                df,
                column_config={
                    "Year": st.column_config.NumberColumn(format="%d")
                },
            )

    # i. Bar Chart
    st.header("Churn Predictions Bar Chart")
    bar_data = df["pred_churn"].value_counts()
    fig_bar = px.bar(bar_data, x=bar_data.index, y=bar_data.values, color=bar_data.index,
                     labels={'x': 'Churn Predictions', 'y': 'Count'},
                     title="Churn Predictions")
    st.plotly_chart(fig_bar)

    # ii. Confusion Matrix
    st.header("Confusion Matrix")
    y_true = df['pred_churn']
    y_pred_proba = df['pred_probability']
    threshold = 0.5
    y_pred_binary = (y_pred_proba > threshold).astype(int)

    y_true = y_true.fillna(0)

    # Confusion Matrix
    cm = confusion_matrix(y_true, y_pred_binary)

    # Classification Report
    class_report = classification_report(y_true, y_pred_binary)

    # Display Confusion Matrix and Classification Report
    st.subheader("Confusion Matrix:")
    st.text("Rows: Actual Classes, Columns: Predicted Classes")
    st.write(cm)

    st.subheader("Classification Report:")
    st.write(class_report)

    # iii. ROC Curve
    st.header("ROC Curve")
    fpr, tpr, thresholds = roc_curve(y_true, y_pred_proba)
    roc_auc = auc(fpr, tpr)

    fig_roc = go.Figure()
    fig_roc.add_trace(go.Scatter(x=fpr, y=tpr, mode='lines', name='ROC curve (area = {:.2f})'.format(roc_auc)))
    fig_roc.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode='lines', name='Random', line=dict(dash='dash')))
    fig_roc.update_layout(xaxis_title='False Positive Rate', yaxis_title='True Positive Rate',
                          title='Receiver Operating Characteristic (ROC) Curve')
    st.plotly_chart(fig_roc)

    # iv. Precision-Recall Curve
    st.header("Precision-Recall Curve")
    precision, recall, _ = precision_recall_curve(y_true, y_pred_proba)
    fig_pr = go.Figure()
    fig_pr.add_trace(go.Scatter(x=recall, y=precision, mode='lines', name='PR curve'))
    fig_pr.update_layout(xaxis_title='Recall', yaxis_title='Precision', title='Precision-Recall Curve')
    st.plotly_chart(fig_pr)

st.write("This is the Analyzed Predictions dashboard.")