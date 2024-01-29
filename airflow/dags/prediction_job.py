from datetime import timedelta
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
import pandas as pd
import logging
import requests
import os

API_URL = "http://host.docker.internal:8050/predict/"
folder_path = "/opt/data/good"


@dag(
    dag_id='prediction_job',
    description='Take files and output predictions',
    tags=['dsp', 'prediction_job'],
    schedule=timedelta(minutes=1),
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
        prediction_data = {}
        for _, row in df.iterrows():
            prediction_data = {
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
        response = requests.post(
            API_URL,
            json=prediction_data
        )

        response_data = response.json()
        logging.info(f'{response_data}')

    df_to_predict = check_for_new_data(folder_path)
    make_predictions(df_to_predict)


scheduled_job_dag = prediction_job()
