import datetime
import streamlit as st
import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
import requests
from dotenv import load_dotenv
from sqlalchemy import create_engine, update, MetaData, Table, Column, Integer, String
from pathlib import Path
from email.mime.text import MIMEText
import smtplib
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

def is_user_logged_in():
    return 'is_logged_in' in st.session_state


# Function to log in the user
def login(username, password):
    # Replace this with your actual authentication logic
    return username == 'admin' and password == 'admin'

# Load environment variables from .env file
env_path = Path('.') / 'myenv.env'
load_dotenv(dotenv_path=env_path)

dummy_prediction_data = {"user_id": 1, "prediction": "churn", "probability": 0.75}
user_email = "duong.tranhn1102@gmail.com"


def send_email(sender, recipient, subject, message):
    # Create the message
    message = MIMEText(message)
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = recipient

    # Establish a connection with the SMTP server
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(user_email, "ulws pdlo avlh oggs")
        server.sendmail(sender, recipient, message.as_string())


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


def submit_feedback(selected_customers, used_feedback):
    db_config = {
        "user": "postgres",
        "password": "0",
        "host": "localhost",
        "port": "5432",
        "database": "churn"
    }
    # print("Selected Customers:", selected_customers)

    engine = create_engine("postgresql://postgres:0@localhost:5432/churn")

    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        if not selected_customers:
            st.warning("No records found for selected customers.")
        else:
            for user in selected_customers:
                user_fb = ModelFeedbacks(
                    user_id=user,
                    feedbacks=used_feedback
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

    # Check if the user is logged in
    if not is_user_logged_in():
        st.warning("Please log in to access this page.")
        return

    # Logout button
    if st.button("Logout"):
        # Clear session state to log out the user
        del st.session_state.is_logged_in
        st.success("Logout successful!")
        st.experimental_rerun()

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

    # Check if the user is logged in
    if not is_user_logged_in():
        st.warning("Please log in to access this page.")
        return

    # Logout button
    if st.button("Logout"):
        # Clear session state to log out the user
        del st.session_state.is_logged_in
        st.success("Logout successful!")
        st.experimental_rerun()

    start_date = st.date_input("Start Date")
    today = datetime.date.today()
    end_date = st.date_input("End Date", max_value=today + datetime.timedelta(days=1))

    data = {
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "limit": 25
    }

    response = requests.get(api_url, json=data)
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

        feedback_text = st.text_area("Provide Feedback:")

        if st.button("Confirm Selected Customers"):
            st.write(selected_customers)

        if feedback_text and st.button("Submit Feedback"):
            submit_feedback(selected_customers, feedback_text)
            st.toast("Feedbacks sent!", icon="🎉")

        



def send_recommendations_page():
    st.title("Send Recommendation to Customer Service")

    # Check if the user is logged in
    if not is_user_logged_in():
        st.warning("Please log in to access this page.")
        return

    # Logout button
    if st.button("Logout"):
        # Clear session state to log out the user
        del st.session_state.is_logged_in
        st.success("Logout successful!")
        st.experimental_rerun()
    

    to_address = st.text_input("Recipient Email")
    subject = st.text_input("Subject")
    message = st.text_area("Message")

    if st.button("Send Email"):
        if send_email(user_email, to_address, subject, message):
            print("Sent!")
        st.toast("Email sent successfully.", icon="🎉")


# Function to display login page
def display_login_page():
    st.title("Login")
    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")

    if st.button("Login"):
        if login(username, password):
            # Set session state to indicate the user is logged in
            st.session_state.is_logged_in = True
            st.success("Login successful!")
        else:
            st.error("Invalid username or password. Please try again.")


# Main function
def main():
    st.set_page_config(page_title="Churn Prediction Platform", page_icon="📊")

    # Check if the user is logged in
    if not is_user_logged_in():
        # Display login page if not logged in
        display_login_page()
        return

    # User is logged in, display the selected page
    page = st.sidebar.selectbox("Select a page:", ["Interactive Dashboard", "Past Predictions", "Send Recommendations"])

    if page == "Interactive Dashboard":
        interactive_dashboard()
    elif page == "Past Predictions":
        past_predictions_page(GET_URL)
    elif page == "Send Recommendations":
        send_recommendations_page()


if __name__ == "__main__":
    main()