from email.mime.text import MIMEText
import smtplib

DB_URL = "postgresql://postgres:khanhduong@host.docker.internal:5432/dl"
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
