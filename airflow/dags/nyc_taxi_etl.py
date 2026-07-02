from datetime import datetime, timedelta
import os
import sys

from airflow import DAG
from airflow.operators.python import PythonOperator

sys.path.append("/opt/airflow/project/src")

from download_data import download_taxi_data
from transform import transform_taxi_data
from upload_to_s3 import upload_processed_files_to_s3


def validate_processed_outputs():
    required_files = [
        "/opt/airflow/data/processed/cleaned_taxi_trips.csv",
        "/opt/airflow/data/processed/cleaned_taxi_trips.parquet",
        "/opt/airflow/data/processed/daily_trip_summary.csv",
        "/opt/airflow/data/processed/payment_type_summary.csv",
    ]

    missing_files = []

    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)

    if missing_files:
        raise FileNotFoundError(f"Missing processed files: {missing_files}")

    print("All processed output files were found successfully.")


default_args = {
    "owner": "data-engineering",
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="nyc_taxi_etl_pipeline",
    description="NYC Taxi ETL pipeline using Python, Docker, Airflow, and AWS S3",
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["nyc-taxi", "etl", "s3"],
) as dag:

    download_task = PythonOperator(
        task_id="download_nyc_taxi_data",
        python_callable=download_taxi_data,
    )

    transform_task = PythonOperator(
        task_id="transform_nyc_taxi_data",
        python_callable=transform_taxi_data,
    )

    validate_outputs_task = PythonOperator(
        task_id="validate_processed_outputs",
        python_callable=validate_processed_outputs,
    )

    upload_task = PythonOperator(
        task_id="upload_outputs_to_s3",
        python_callable=upload_processed_files_to_s3,
    )

    download_task >> transform_task >> validate_outputs_task >> upload_task