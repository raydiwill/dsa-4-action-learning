from email.mime.text import MIMEText
import smtplib

GET_URL = "http://localhost:8050/past-predictions/"
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