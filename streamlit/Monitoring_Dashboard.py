import pandas as pd
import psycopg2
import streamlit as st
import plotly.express as px

@st.cache
def load_data(file):
    data = pd.read_csv(file)
    return data

def save_to_database(df):
    conn = psycopg2.connect(
        dbname='action-learning',
        user='postgres',
        password='sup3r',
        host='localhost',
        port='5432'
    )
    cur = conn.cursor()
    for index, row in df.iterrows():
        cur.execute(
            "INSERT INTO customers_report (user_id, model_pred, strategy, communication_method) VALUES (%s, %s, %s, %s)",
            (row['user_id'], row['model_pred'], row['strategy'], row['communication_method'])
        )
    conn.commit()

def run():
    st.header("Monitoring Dashboard")

    # Use a unique key for the file uploader widget
    uploaded_file = st.sidebar.file_uploader("Please choose a file", key="monitoring_file_uploader")
    
    if uploaded_file is not None:
        df = load_data(uploaded_file)
        st.write("Columns in DataFrame:", df.columns)
        save_to_database(df)

        # Generate graph
        fig = px.bar(df, x='user_id', y='model_pred',
                     color='strategy', barmode='group',
                     title="User Churn Prediction with Retention Strategies")
        
        # Display graph in Streamlit app
        st.plotly_chart(fig)
    else:
        st.warning("No file uploaded.")

    st.write("This is the Monitoring dashboard.")

# Call run function directly
run()
