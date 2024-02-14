from email.mime.text import MIMEText
import smtplib

default_folder = "/opt/data/default"
good_folder = "/opt/data/good"
failed_folder = "/opt/data/bad"

DB_URL = "postgresql://postgres:khanhduong@host.docker.internal:5432/dl"
POST_URL = "http://host.docker.internal:8050/predict/"
GET_URL = "http://host.docker.internal:8050/past-predictions/"

user_email = "duong.tranhn1102@gmail.com"
recipient_email = "trankhanhduong112@gmail.com"


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
