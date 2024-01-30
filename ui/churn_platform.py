import datetime
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, update, MetaData, Table, Column, Integer, String
from sqlalchemy.exc import SQLAlchemyError
import requests
from dotenv import load_dotenv
from sqlalchemy import create_engine, update, MetaData, Table, Column, Integer, String
#from ..api.config import settings  
from pathlib import Path
import os


GET_URL = "http://localhost:8050/past-predictions/"


# Load environment variables from .env file
env_path = Path('.') / 'myenv.env'
load_dotenv(dotenv_path=env_path)

dummy_prediction_data = {"user_id": 1, "prediction": "churn", "probability": 0.75}

def fetch_data_from_api(api_url, data):
    try:
        url = api_url
        response = requests.get(url, json=data)
        if response.status_code == 200:
            data = response.json()
            return pd.DataFrame(data)
        else:
            st.error(f"Error fetching data from API. Status code: {response.status_code}")
    except Exception as e:
        st.error(f"Error fetching data from API: {e}")
    return pd.DataFrame()


def get_predictions():
    return dummy_prediction_data


def submit_feedback(selected_customers, feedback):
    db_config = {
        "user": "postgres",
        "password": "0",
        "host": "localhost",
        "port": "5432",
        "database": "churn"
    }

    # Connection to the database
    engine = create_engine(f"postgresql+psycopg2://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")

    # Load table metadata
    metadata = MetaData()
    test_pred_table = Table('churn.test_pred', metadata, autoload_with=engine)

    # Iterate over selected customers and update feedback in the database
    for user_id in selected_customers:
        feedback_data = {
            "user_id": user_id,
            "feedback": feedback
        }

        try:
            # Build the update statement
            stmt = update(test_pred_table).where(test_pred_table.c.user_id == feedback_data['user_id']).values(feedback=feedback_data['feedback'])

            # Execute the update statement
            result = engine.execute(stmt)
            
            # Check if the update was successful
            if result.rowcount > 0:
                st.success(f"Feedback updated for user {user_id}")
            else:
                st.warning(f"No records updated for user {user_id}")

        except SQLAlchemyError as e:
            st.error(f"Error during update: {e}")

    # Close the database connection
    engine.dispose()

    st.success("Feedback submitted successfully.")

def interactive_dashboard():
    st.title("Churn Prediction Dashboard")

    predictions = get_predictions()

    st.subheader("Analyze Returned Predictions:")
    st.write(f"Customer ID: {predictions['user_id']}")
    st.write(f"Prediction: {predictions['prediction']}")
    st.write(f"Probability: {predictions['probability']}")

    if predictions['prediction'] == 'churn' and predictions['probability'] > 0.5:
        st.warning("Churn predicted with high probability. Recommend retention strategies.")

    st.subheader("Customer Profiling:")
    # Add customer profiling details here

    st.subheader("CS Team Reports:")
    # Display feedback form here


def filter_customers_by_risk(past_predictions, risk):
    return past_predictions[past_predictions['risk'].str.lower() == risk.lower()]


def past_predictions_page(api_url):
    st.title("Past Predictions")

    start_date = st.date_input("Start Date")
    today = datetime.date.today()
    end_date = st.date_input("End Date",
                             max_value=today + datetime.timedelta(days=1))
    
    data = {
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d")
        #"pred_source": prediction_source
    }
    
    response = requests.get(api_url, json=data)
    print(response)
    past_predictions = pd.DataFrame(response.json())

    # Display a table with fetched data
    st.table(past_predictions)

    # Filter customers based on risk level
    risk_level_filter = st.selectbox("Filter by Risk Level:", ["All", "High", "Low"])
    if risk_level_filter != "All":
        filtered_customers = past_predictions[past_predictions['pred_risk'].str.lower() == risk_level_filter.lower()]

        # Display a different table for filtered customers
        st.subheader(f"Filtered Customers (Risk Level: {risk_level_filter}):")
        st.table(filtered_customers)

        # Selection mechanism
        selected_customers = st.multiselect("Select customers to provide feedback:", filtered_customers["user_id"].tolist())

        # Confirm selected choices with a button
        if st.button("Confirm Selected Customers"):
            # Popup for feedback
            feedback_text = st.text_area("Provide Feedback:")
            if st.button("Submit Feedback"):
                submit_feedback(selected_customers, feedback_text)


def main():
    st.set_page_config(page_title="Churn Prediction Platform", page_icon="📊")

    page = st.sidebar.selectbox("Select a page:", ["Interactive Dashboard", "Past Predictions"])

    if page == "Interactive Dashboard":
        interactive_dashboard()
    elif page == "Past Predictions":
        # Update the API URL based on your actual API endpoint
        past_predictions_page(GET_URL)

if __name__ == "__main__":
    main()
