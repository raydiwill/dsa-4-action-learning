from datetime import timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from email.mime.text import MIMEText
import datetime
import random
import glob
import os
import pandas as pd
import shutil
import great_expectations as gx
import logging
import smtplib

import sys
sys.path.append('/opt/api')
from models import *
from setup_db import *

DB_URL = "postgresql://postgres:khanhduong@host.docker.internal:5432/mydbs"
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


@dag(
    dag_id='data_ingestion',
    description='Take files and validate the quality',
    tags=['dsp', 'validate', 'ingestion'],
    schedule_interval='*/10 * * * * *',
    #schedule=timedelta(minutes=0.5),
    start_date=days_ago(n=0, hour=1)
)
def data_ingestion():
    default_folder = "/opt/data/default"
    good_folder = "/opt/data/good"
    failed_folder = "/opt/data/bad"

    @task
    def read_file():
        file_pattern = os.path.join(default_folder, "*.csv")
        file_paths = glob.glob(file_pattern)
        logging.info(f'{file_paths}')
        file_paths = [f for f in file_paths if
                      not os.path.basename(f).startswith('processed_')]

        file_path = random.choice(file_paths)
        logging.info(f'Chosen file: {file_path}')

        # Define the new name for the processed file
        processed_file_name = "processed_" + os.path.basename(file_path)
        processed_file_path = os.path.join(default_folder,
                                           processed_file_name)

        os.rename(file_path, processed_file_path)

        return processed_file_path

    @task
    def validate_data(file):
        context = gx.get_context()
        validator = context.sources.pandas_default.read_csv(file)

        validator.expect_column_values_to_not_be_null(
            "user_id", result_format={'result_format': 'SUMMARY'}
        )

        validator.expect_column_values_to_be_of_type(
            "REGION", "object",
            result_format={'result_format': 'SUMMARY'}
        )

        """
        validator.expect_column_values_to_not_be_null(
            "REGION", mostly=0.40,
            result_format={'result_format': 'SUMMARY'}
        )
        """

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
            "MONTANT", min_value=0,
            result_format={'result_format': 'SUMMARY'}
        )

        """
        validator.expect_column_values_to_not_be_null(
            "MONTANT", mostly=0.40,
            result_format={'result_format': 'SUMMARY'}
        )
        """

        validator.expect_column_values_to_be_of_type(
            "FREQUENCE_RECH", "float64",
            result_format={'result_format': 'SUMMARY'}
        )

        validator.expect_column_values_to_be_between(
            "FREQUENCE_RECH", min_value=0,
            result_format={'result_format': 'SUMMARY'}
        )

        """
        validator.expect_column_values_to_not_be_null(
            "FREQUENCE_RECH", mostly=0.40,
            result_format={'result_format': 'SUMMARY'}
        )
        """

        validator.expect_column_values_to_be_of_type(
            "REVENUE", "float64",
            result_format={'result_format': 'SUMMARY'}
        )

        validator.expect_column_values_to_be_between(
            "REVENUE", min_value=0,
            result_format={'result_format': 'SUMMARY'}
        )

        """
        validator.expect_column_values_to_not_be_null(
            "REVENUE", mostly=0.40,
            result_format={'result_format': 'SUMMARY'}
        )
        """

        validator.expect_column_values_to_be_of_type(
            "ARPU_SEGMENT", "float64",
            result_format={'result_format': 'SUMMARY'}
        )

        validator.expect_column_values_to_be_between(
            "ARPU_SEGMENT", min_value=0,
            result_format={'result_format': 'SUMMARY'}
        )

        """
        validator.expect_column_values_to_not_be_null(
            "ARPU_SEGMENT", mostly=0.40,
            result_format={'result_format': 'SUMMARY'}
        )
        """

        validator.expect_column_values_to_be_of_type(
            "FREQUENCE", "float64",
            result_format={'result_format': 'SUMMARY'}
        )

        validator.expect_column_values_to_be_between(
            "FREQUENCE", min_value=0,
            result_format={'result_format': 'SUMMARY'}
        )

        """
        validator.expect_column_values_to_not_be_null(
            "FREQUENCE", mostly=0.40,
            result_format={'result_format': 'SUMMARY'}
        )
        """

        validator.expect_column_values_to_be_of_type(
            "DATA_VOLUME", "float64",
            result_format={'result_format': 'SUMMARY'}
        )

        validator.expect_column_values_to_be_between(
            "DATA_VOLUME", min_value=0,
            result_format={'result_format': 'SUMMARY'}
        )

        """
        validator.expect_column_values_to_not_be_null(
            "DATA_VOLUME", mostly=0.40,
            result_format={'result_format': 'SUMMARY'}
        )
        """

        validator.expect_column_values_to_be_of_type(
            "ON_NET", "float64",
            result_format={'result_format': 'SUMMARY'}
        )

        validator.expect_column_values_to_be_between(
            "ON_NET", min_value=0,
            result_format={'result_format': 'SUMMARY'}
        )

        """
        validator.expect_column_values_to_not_be_null(
            "ON_NET", mostly=0.40,
            result_format={'result_format': 'SUMMARY'}
        )
        """

        validator.expect_column_values_to_be_of_type(
            "ORANGE", "float64",
            result_format={'result_format': 'SUMMARY'}
        )

        validator.expect_column_values_to_be_between(
            "ORANGE", min_value=0,
            result_format={'result_format': 'SUMMARY'}
        )

        """
        validator.expect_column_values_to_not_be_null(
            "ORANGE", mostly=0.40,
            result_format={'result_format': 'SUMMARY'}
        )
        """

        validator.expect_column_values_to_be_of_type(
            "TIGO", "float64",
            result_format={'result_format': 'SUMMARY'}
        )

        validator.expect_column_values_to_be_between(
            "TIGO", min_value=0,
            result_format={'result_format': 'SUMMARY'}
        )

        """
        validator.expect_column_values_to_not_be_null(
            "TIGO", mostly=0.40,
            result_format={'result_format': 'SUMMARY'}
        )
        """

        validator.expect_column_values_to_be_of_type(
            "REGULARITY", "int64",
            result_format={'result_format': 'SUMMARY'}
        )

        validator.expect_column_values_to_be_between(
            "REGULARITY", min_value=0,
            result_format={'result_format': 'SUMMARY'}
        )

        """
        validator.expect_column_values_to_not_be_null(
            "REGULARITY", mostly=0.40,
            result_format={'result_format': 'SUMMARY'}
        )
        """

        validator.expect_column_values_to_be_of_type(
            "TOP_PACK", "object",
            result_format={'result_format': 'SUMMARY'}
        )

        validator.expect_column_values_to_be_between(
            "TOP_PACK", min_value=0,
            result_format={'result_format': 'SUMMARY'}
        )

        """
        validator.expect_column_values_to_not_be_null(
            "TOP_PACK", mostly=0.40,
            result_format={'result_format': 'SUMMARY'}
        )
        """

        validator.expect_column_values_to_be_of_type(
            "FREQ_TOP_PACK", "float64",
            result_format={'result_format': 'SUMMARY'}
        )

        validator.expect_column_values_to_be_between(
            "FREQ_TOP_PACK", min_value=0,
            result_format={'result_format': 'SUMMARY'}
        )

        """
        validator.expect_column_values_to_not_be_null(
            "FREQ_TOP_PACK", mostly=0.40,
            result_format={'result_format': 'SUMMARY'}
        )
        """

        validator_result = validator.validate()
        return {"file": file, "validator_result": validator_result}

    @task
    def raise_alert(validator_output):
        validator_result = validator_output["validator_result"]
        sender = user_email
        recipient = "trankhanhduong112@gmail.com"
        subject = "Data Quality Issues"

        failed_tests = [result for result in validator_result["results"] if
                        not result["success"]]
        if failed_tests:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            message = f"Dear Engineering team,\n\n"
            message += f"Data Quality Alert - {timestamp}\n\n"
            message += "The following data quality checks have failed:\n\n"

            for test in failed_tests:
                message += (f"- Expectation: "
                            f"{test['expectation_config']['expectation_type']}\n")
                message += (f"- Column: "
                            f"{test['expectation_config']['kwargs']['column']}\n")
                message += (f"- Details: "
                            f"{test['result']['partial_unexpected_list']}"
                            f"\n\n")

            message += ("Please review the validation results and "
                        "address the issues as soon as possible.\n")
            message += (f'\nBest Regards,\n'
                        f'[Name]\n'
                        f'ML engineer\n'
                        f'[Company]')
            send_email(sender, recipient, subject, message)
            logging.info(f'Email sent!')
        else:
            logging.info('No data quality issues detected.')

    @task
    def split_file(validator_output, folder_b, folder_c):
        file = validator_output["file"]
        validator_result = validator_output["validator_result"]
        df = pd.read_csv(file)
        problem_rows = []

        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        for result in validator_result["results"]:
            if not result["success"]:
                problem_rows.extend(
                    result["result"]["partial_unexpected_index_list"])

        if not problem_rows:
            shutil.move(file, folder_c)
        else:
            df_problems = df.loc[problem_rows]
            df_no_problems = df.drop(problem_rows)

            problems_file_path = (
                os.path.join(folder_b,
                             f"file_with_problems_"
                             f"{timestamp}_{os.path.basename(file)}"))
            no_problems_file_path = (
                os.path.join(folder_c,
                             f"file_without_problems_"
                             f"{os.path.basename(file)}"))

            df_problems.to_csv(problems_file_path, index=False)
            df_no_problems.to_csv(no_problems_file_path, index=False)

    @task
    def save_quality_issues(validator_output, db_url):
        validator_result = validator_output["validator_result"]
        engine = create_engine(db_url)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()

        file_name = (
            os.path.basename(validator_result
                             ["meta"]["batch_spec"]
                             ["reader_options"]["filepath_or_buffer"]))
        for result in validator_result["results"]:
            if not result["success"]:
                column = result["expectation_config"]["kwargs"]["column"]
                expectation_type = result["expectation_config"][
                    "expectation_type"]
                unexpected_values = (
                    str(result["result"]["partial_unexpected_list"]))

                stat = ProblemStats(
                    file_name=file_name,
                    column=column,
                    expectation_type=expectation_type,
                    unexpected_values=unexpected_values
                )
                session.add(stat)

            session.commit()
            session.close()

    # Task
    chosen_file = read_file()
    validate = validate_data(chosen_file)
    raise_alert(validate)
    split_file(validate, failed_folder, good_folder)
    save_quality_issues(validate, DB_URL)


ingestion_dag = data_ingestion()
