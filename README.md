🌦️ Weather ETL Pipeline (Production-Style Data Engineering Project)
🚀 Project Overview

This project is a production-style ETL pipeline built using Apache Airflow that:

Extracts real-time weather data from OpenWeatherMap API

Validates schema and data quality

Transforms and converts units

Stores partitioned Parquet files in AWS S3

Supports dev/prod environments

Implements error handling and retries

This project demonstrates real-world data engineering practices including:

Airflow DAG orchestration

Cloud storage (AWS S3)

Schema validation

Data quality checks

Partitioned Parquet storage

Environment-based configuration

🏗 Architecture Diagram

                +-------------------+
                | OpenWeatherMap API|
                +-------------------+
                          |
                          v
                +-------------------+
                |  Airflow DAG      |
                |-------------------|
                | 1. HttpSensor     |
                | 2. Extract Task   |
                | 3. Transform Task |
                +-------------------+
                          |
                          v
                +-------------------+
                | Schema Validation |
                | + Data Quality    |
                +-------------------+
                          |
                          v
                +-------------------+
                | Transform + Clean |
                +-------------------+
                          |
                          v
                +-------------------+
                | Partitioned       |
                | Parquet Files 
                  email| alerts
                +-------------------+
                          |
                          v
                +-------------------+
                | AWS S3 Bucket     |
                | (dev / prod)      |
                +-------------------+

📦 Tech Stack

Python 3.10

Apache Airflow

Pandas

PyArrow

AWS S3

s3fs

OpenWeatherMap API

🔁 ETL Flow
1️⃣ Extract

Uses HttpSensor to check API availability

Uses SimpleHttpOperator to fetch JSON weather data

2️⃣ Transform

Convert Kelvin to Fahrenheit

Extract relevant fields

Create structured dataframe

3️⃣ Schema Validation

Validates:

Required JSON keys

Required main fields

Temperature realistic range (200K–350K)

Humidity range (0–100)

Wind speed non-negative


4️⃣ Load

Stores partitioned Parquet in S3

Partitioned by execution date
🗂 S3 Storage Structure
weather/
 ├── year=2026/
 │    ├── month=02/
 │    │    ├── day=14/
 │    │    │    ├── weather.parquet
 
✨ Additional Features Implemented
📧 Email Alerts

Email notifications configured for task failures

Alerts triggered automatically on retry exhaustion

Uses Airflow’s built-in email configuration

Enables production-grade monitoring

🌍 Parameterized City

The pipeline supports dynamic city configuration via Airflow Variables or environment variables.
🌍 Environment Configuration

Bucket selection is dynamic based on environmen
