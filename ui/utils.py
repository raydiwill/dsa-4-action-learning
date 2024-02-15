from email.mime.text import MIMEText
import streamlit as st
import pandas as pd
import requests
import smtplib

GET_URL = "http://localhost:8050/past-predictions/"
user_email = "duong.tranhn1102@gmail.com"


def is_user_logged_in():
    return 'is_logged_in' in st.session_state


# Function to log in the user
def login(username, password):
    # Replace this with your actual authentication logic
    return username == 'admin' and password == 'admin'


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
            st.error(f"Error fetching data from API. Status code: {response.status_code}")
    except Exception as e:
        st.error(f"Error fetching data from API: {e}")
    return pd.DataFrame()