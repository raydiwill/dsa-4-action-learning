from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path
from email.mime.text import MIMEText
from sqlalchemy import create_engine
import streamlit as st
import pandas as pd
import requests
import smtplib
import sys

sys.path.append("../")
from api.models import *
from api.config import *
# from api.setup_db import get_db, SessionLocal


GET_URL = "http://localhost:8050/past-predictions/"
user_email = "duong.tranhn1102@gmail.com"

# Load environment variables from .env file
env_path = Path("..") / "myenv.env"
load_dotenv(dotenv_path=env_path)


def is_user_logged_in():
    return "is_logged_in" in st.session_state


# Function to log in the user
def login(username, password):
    # Replace this with your actual authentication logic
    return username == "admin" and password == "admin"


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
        response = requests.get(api_url, json=data)
        if response.status_code == 200:
            data = response.json()
            return pd.DataFrame(data)
        else:
            st.error(
                f"Error fetching data from API. Status code: {response.status_code}"
            )
    except Exception as e:
        st.error(f"Error fetching data from API: {e}")
    return pd.DataFrame()


def save_to_database(df, table_name, database_uri):
    engine = create_engine(database_uri)
    df.to_sql(table_name, engine, if_exists="replace", index=False)


# Function to generate recommendations
def generate_recommendations():
    return [
        "1. Personalize communication with high-risk customers.",
        "2. Offer loyalty programs for long-term customers.",
        "3. Review and adjust pricing strategies for popular service packages.",
        "4. Enhance customer service and support.",
        "5. Implement targeted marketing campaigns in high-churn regions.",
    ]


def submit_feedback(selected_customers, used_feedback):
    engine = create_engine(settings.DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        if not selected_customers:
            st.warning("No records found for selected customers.")
        else:
            for user in selected_customers:
                user_fb = ModelFeedbacks(user_id=user, feedbacks=used_feedback)
                session.add(user_fb)

            session.commit()
            st.success("Feedback submitted successfully.")

    except SQLAlchemyError as e:
        session.rollback()
        st.error(f"Error during feedback submission: {e}")
    finally:
        session.close()
