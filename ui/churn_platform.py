import datetime
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, update, MetaData, Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
import requests
from dotenv import load_dotenv
from sqlalchemy import create_engine, update, MetaData, Table, Column, Integer, String
#from ..api.config import settings  
from pathlib import Path
import sys
sys.path.append('../')
from api.models import *
#from api.setup_db import get_db, SessionLocal
#from api.config import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import streamlit as st
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


def submit_feedback(selected_customers, feedback):
    db_config = {
        "user": "postgres",
        "password": "0",
        "host": "localhost",
        "port": "5432",
        "database": "churn"
    }
    #print("Selected Customers:", selected_customers)

    engine = create_engine(f"postgresql://postges:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")

    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        if not selected_customers:
            st.warning("No records found for selected customers.")
        else:
            user_fb = ModelFeedbacks(
                user_id=selected_customers,
                feedback=feedback
            )
            session.add(user_fb)

            session.commit()
            st.success("Feedback submitted successfully.")

    except SQLAlchemyError as e:
        session.rollback()
        st.error(f"Error during feedback submission: {e}")

    finally:
        session.close()


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
        st.write(selected_customers)
        #st.write(type(selected_customers))
        # Confirm selected choices with a button
        if st.button("Confirm Selected Customers"):
            # Popup for feedback
            feedback_text = st.text_area("Provide Feedback:")
            st.write(feedback_text)
            if st.button("Submit Feedback"):
                submit_feedback(selected_customers, feedback_text)
                st.toast("Feedbacks sent!", icon="🎉")


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
