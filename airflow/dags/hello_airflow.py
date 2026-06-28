from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def hello():
    print("===================================")
    print("Hello from Apache Airflow!")
    print("Your ETL project is now orchestrated.")
    print("===================================")


with DAG(
    dag_id="hello_airflow",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["tutorial"],
) as dag:

    hello_task = PythonOperator(
        task_id="hello_task",
        python_callable=hello,
    )