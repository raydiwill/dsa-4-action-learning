from email.mime.text import MIMEText
import great_expectations as gx
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


def gx_validation(file):
    context = gx.get_context()
    validator = context.sources.pandas_default.read_csv(file)

    validator.expect_column_values_to_not_be_null(
        "user_id", result_format={'result_format': 'SUMMARY'}
    )

    validator.expect_column_values_to_be_of_type(
        "REGION", "object",
        result_format={'result_format': 'SUMMARY'}
    )

    validator.expect_column_values_to_be_of_type(
        "TENURE", "object",
        result_format={'result_format': 'SUMMARY'}
    )

    validator.expect_column_values_to_not_be_null(
        "TENURE",
        result_format={'result_format': 'SUMMARY'}
    )

    validator.expect_column_values_to_be_of_type(
        "MONTANT", "float64",
        result_format={'result_format': 'SUMMARY'}
    )

    validator.expect_column_values_to_be_between(
        "MONTANT", min_value=0.0,
        result_format={'result_format': 'SUMMARY'}
    )

    validator.expect_column_values_to_be_of_type(
        "FREQUENCE_RECH", "float64",
        result_format={'result_format': 'SUMMARY'}
    )

    validator.expect_column_values_to_be_between(
        "FREQUENCE_RECH", min_value=0.0,
        result_format={'result_format': 'SUMMARY'}
    )

    validator.expect_column_values_to_be_of_type(
        "REVENUE", "float64",
        result_format={'result_format': 'SUMMARY'}
    )

    validator.expect_column_values_to_be_between(
        "REVENUE", min_value=0.0,
        result_format={'result_format': 'SUMMARY'}
    )

    validator.expect_column_values_to_be_of_type(
        "ARPU_SEGMENT", "float64",
        result_format={'result_format': 'SUMMARY'}
    )

    validator.expect_column_values_to_be_between(
        "ARPU_SEGMENT", min_value=0.0,
        result_format={'result_format': 'SUMMARY'}
    )

    validator.expect_column_values_to_be_of_type(
        "FREQUENCE", "float64",
        result_format={'result_format': 'SUMMARY'}
    )

    validator.expect_column_values_to_be_between(
        "FREQUENCE", min_value=0.0,
        result_format={'result_format': 'SUMMARY'}
    )

    validator.expect_column_values_to_be_of_type(
        "DATA_VOLUME", "float64",
        result_format={'result_format': 'SUMMARY'}
    )

    validator.expect_column_values_to_be_between(
        "DATA_VOLUME", min_value=0.0,
        result_format={'result_format': 'SUMMARY'}
    )

    validator.expect_column_values_to_be_of_type(
        "ON_NET", "float64",
        result_format={'result_format': 'SUMMARY'}
    )

    validator.expect_column_values_to_be_between(
        "ON_NET", min_value=0.0,
        result_format={'result_format': 'SUMMARY'}
    )

    validator.expect_column_values_to_be_of_type(
        "ORANGE", "float64",
        result_format={'result_format': 'SUMMARY'}
    )

    validator.expect_column_values_to_be_between(
        "ORANGE", min_value=0.0,
        result_format={'result_format': 'SUMMARY'}
    )

    validator.expect_column_values_to_be_of_type(
        "TIGO", "float64",
        result_format={'result_format': 'SUMMARY'}
    )

    validator.expect_column_values_to_be_between(
        "TIGO", min_value=0.0,
        result_format={'result_format': 'SUMMARY'}
    )

    validator.expect_column_values_to_be_of_type(
        "REGULARITY", "int64",
        result_format={'result_format': 'SUMMARY'}
    )

    validator.expect_column_values_to_be_between(
        "REGULARITY", min_value=0,
        result_format={'result_format': 'SUMMARY'}
    )

    validator.expect_column_values_to_be_of_type(
        "TOP_PACK", "object",
        result_format={'result_format': 'SUMMARY'}
    )

    validator.expect_column_values_to_be_of_type(
        "FREQ_TOP_PACK", "float64",
        result_format={'result_format': 'SUMMARY'}
    )

    validator.expect_column_values_to_be_between(
        "FREQ_TOP_PACK", min_value=0.0,
        result_format={'result_format': 'SUMMARY'}
    )

    validator_result = validator.validate()
    return {"file": file, "validator_result": validator_result}
