from datetime import datetime, timedelta
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from email.mime.text import MIMEText
import pandas as pd
import logging
import requests
import os
import smtplib

POST_URL = "http://host.docker.internal:8050/predict/"
GET_URL = "http://host.docker.internal:8050/past-predictions/"
folder_path = "/opt/data/good"
user_email = "duong.tranhn1102@gmail.com"
dates = {
    "start_date": (datetime.today()).strftime(
        "%Y-%m-%d"),
    "end_date": (datetime.now() + timedelta(days=1)).strftime(
        "%Y-%m-%d")
}


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


@dag(
    dag_id='prediction_job',
    description='Take files and output predictions',
    tags=['dsp', 'prediction_job'],
    schedule_interval="0 9 1 * *",
    #schedule=timedelta(minutes=30),
    start_date=days_ago(n=0, hour=1),
    catchup=False
)
def prediction_job():
    @task
    def check_for_new_data(path):
        csv_files = [file for file in os.listdir(path) if
                     file.endswith(".csv") and
                     not file.startswith("predicted_")]

        if not csv_files:
            return None

        df_list = []
        for file in csv_files:
            file_path = os.path.join(folder_path, file)
            df_list.append(pd.read_csv(file_path))
            processed_file_path = os.path.join(folder_path,
                                               f'predicted_{file}')
            os.rename(file_path, processed_file_path)

        merged_df = pd.concat(df_list, ignore_index=True)
        return merged_df

    @task
    def make_predictions(df):
        prediction_data = []
        for _, row in df.iterrows():
            row_data = {
                "user_id": row["user_id"],
                "REGION": row["REGION"] if not pd.isna(
                    row["REGION"]) else None,
                "TENURE": row["TENURE"] if not pd.isna(
                    row["TENURE"]) else None,
                "MONTANT": row["MONTANT"] if not pd.isna(
                    row["MONTANT"]) else None,
                "FREQUENCE_RECH": row["FREQUENCE_RECH"] if not pd.isna(
                    row["FREQUENCE_RECH"]) else None,
                "REVENUE": row["REVENUE"] if not pd.isna(
                    row["REVENUE"]) else None,
                "ARPU_SEGMENT": row["ARPU_SEGMENT"] if not pd.isna(
                    row["ARPU_SEGMENT"]) else None,
                "FREQUENCE": row["FREQUENCE"] if not pd.isna(
                    row["FREQUENCE"]) else None,
                "DATA_VOLUME": row["DATA_VOLUME"] if not pd.isna(
                    row["DATA_VOLUME"]) else None,
                "ON_NET": row["ON_NET"] if not pd.isna(
                    row["ON_NET"]) else None,
                "ORANGE": row["ORANGE"] if not pd.isna(
                    row["ORANGE"]) else None,
                "TIGO": row["TIGO"] if not pd.isna(row["TIGO"]) else None,
                "REGULARITY": row["REGULARITY"] if not pd.isna(
                    row["REGULARITY"]) else None,
                "TOP_PACK": row["TOP_PACK"] if not pd.isna(
                    row["TOP_PACK"]) else None,
                "FREQ_TOP_PACK": row["FREQ_TOP_PACK"] if not pd.isna(
                    row["FREQ_TOP_PACK"]) else None,
            }
            prediction_data.append(row_data)

        response = requests.post(
            POST_URL,
            json=prediction_data
        )

        response_data = response.json()
        logging.info(f'{response_data}')
        return response.status_code

    @task
    def get_past_predictions(status):
        response = requests.get(
            GET_URL,
            json=dates
        )

        past_predictions = pd.DataFrame(response.json())
        return past_predictions.to_dict('records')

    @task
    def notify_team(predictions):
        sender = user_email
        recipient = "duong-khanh.tran@epita.fr"

        total_preds = len(predictions)
        churners = len([pred for pred in predictions if
                     pred['pred_churn'] == 1])
        high_risk = [pred for pred in predictions if
                     pred['pred_risk'] == 'High']

        churn_perc = (churners / total_preds) * 100
        if high_risk:
            subject = "High-Risk Churn predictions detected"
            body = (f'Dear Analysis team,\n\n'
                    f'There are {len(high_risk)} high-risk churners detected.'
                    f'\n\nPlease check dashboard.')
            send_email(sender, recipient, subject, body)
            logging.info(f'Email sent!')
        else:
            subject = "Churn predictions notification"
            body = (f'Dear Analysis team,\n'
                    f'\nWe have completed our latest scheduled '
                    f'churn prediction, we wanted to share with you:\n'
                    f'\n    - Date: from {dates["start_date"]} to {dates["end_date"]}'
                    f'\n    - Total number of churners: {churners}'
                    f'\n    - Percentage of churners: {churn_perc}%\n'
                    f'\nWe encourage you to review the attached detailed report for a comprehensive understanding of the churn analysis. Please feel free to reach out if you have any questions or need further clarification on any aspects of this report.\n'
                    f'\nBest Regards,\n'
                    f'[Name]\n'
                    f'ML engineer\n'
                    f'[Company]')
            send_email(sender, recipient, subject, body)
            logging.info(f'Email sent!')

    # Task
    df_to_predict = check_for_new_data(folder_path)
    status_code = make_predictions(df_to_predict)
    pred_dict = get_past_predictions(status_code)
    notify_team(pred_dict)


scheduled_job_dag = prediction_job()
