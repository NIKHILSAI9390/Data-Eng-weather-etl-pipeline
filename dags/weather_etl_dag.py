

from airflow import DAG
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import json
from weather_utils.transform_function import transform_load_data

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2023, 1, 1),
    "email":["nzr0066@auburn.edu"],
    "email_on_failure":True,
    "email_on_retry":False,
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="weather_dag",
    default_args=default_args,
    schedule="@hourly",
    catchup=False,
) as dag:

    is_weather_api_available = HttpSensor(
        task_id="is_weather_api_available",
        http_conn_id="weather_map_api",
        endpoint="data/2.5/weather?q=Stockholm&appid=e10730ddeb6b463d2b7621e8128c6da7",
    )

    extract_weather_data = SimpleHttpOperator(
        task_id="extract_weather_data",
        http_conn_id="weather_map_api",
        endpoint="data/2.5/weather?q=Stockholm&appid=e10730ddeb6b463d2b7621e8128c6da7",
        method="GET",
        response_filter=lambda r: json.loads(r.text),
        log_response=True,
    )

    transform_load_weather_data = PythonOperator(
        task_id="transform_load_weather_data",
        python_callable=transform_load_data,
    )

    is_weather_api_available >> extract_weather_data >> transform_load_weather_data


