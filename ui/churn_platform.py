import datetime
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, update, MetaData, Table, Column, Integer, String
from sqlalchemy.exc import SQLAlchemyError
import streamlit as st
import os


GET_URL = "http://localhost:8050/past-predictions/"


# Load environment variables from .env file
env_path = Path('.') / 'myenv.env'
load_dotenv(dotenv_path=env_path)

dummy_prediction_data = {"user_id": 1, "prediction": "churn", "probability": 0.75}

dummy_past_predictions = [
    {"user_id": 1, "prediction": "churn", "actual_result": "non-churn", "risk_level": "high"},
    {"user_id": 2, "prediction": "non-churn", "actual_result": "non-churn", "risk_level": "low"},
    {"user_id": 3, "prediction": "churn", "actual_result": "churn", "risk_level": "high"},
    {"user_id": 4, "prediction": "non-churn", "actual_result": "non-churn", "risk_level": "low"},
    {"user_id": 5, "prediction": "churn", "actual_result": "churn", "risk_level": "high"}
]

def get_predictions():
    return dummy_prediction_data

from sqlalchemy import create_engine, update, MetaData, Table, Column, Integer, String

from sqlalchemy import create_engine, update, MetaData, Table, Column, Integer, String


def submit_feedback(selected_customers, used_feedback):
    db_config = {
        "user": "postgres",
        "password": "khanhduong",
        "host": "localhost",
        "port": "5432",
        "database": "dl"
    }

    # Connection to the database
    engine = create_engine(f"postgresql+psycopg2://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")

    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

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

    # Fetch data from the database
    past_predictions = fetch_data_from_database()

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

    page = st.sidebar.selectbox("Select a page:", ["Interactive Dashboard", "Past Predictions", "Send Recommendations"])

    if page == "Interactive Dashboard":
        interactive_dashboard()
    elif page == "Past Predictions":
        past_predictions_page()

if __name__ == "__main__":
    main()
