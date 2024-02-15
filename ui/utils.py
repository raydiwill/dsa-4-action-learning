from email.mime.text import MIMEText
import streamlit as st
import smtplib

GET_URL = "http://localhost:8050/past-predictions/"
user_email = "duong.tranhn1102@gmail.com"


def is_user_logged_in():
    return 'is_logged_in' in st.session_state


# Function to log in the user
def login(username, password):
    # Replace this with your actual authentication logic
    return username == 'admin' and password == 'admin'


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