# 🌦️ Weather ETL Pipeline  
### 🚀 Production-Style Data Engineering Project

---

## 🚀 Project Overview

This project is a **production-style ETL pipeline** built using **Apache Airflow** that:

- Extracts real-time weather data from OpenWeatherMap API  
- Validates schema and data quality  
- Transforms and converts units  
- Stores partitioned Parquet files in AWS S3  
- Supports dev/prod environments  
- Implements error handling, retries, and email alerts  

This project demonstrates real-world data engineering practices including:

- Airflow DAG orchestration  
- Cloud storage (AWS S3)  
- Schema validation  
- Data quality checks  
- Partitioned Parquet storage  
- Environment-based configuration  
- Failure alerting & retries  

---

## 🏗 Architecture Diagram

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
            | Parquet Files     |
            | + Email Alerts    |
            +-------------------+
                      |
                      v
            +-------------------+
            | AWS S3 Bucket     |
            | (dev / prod)      |
            +-------------------+

---

## 📦 Tech Stack

- Python 3.10  
- Apache Airflow  
- Pandas  
- PyArrow  
- AWS S3  
- s3fs  
- OpenWeatherMap API  

---

## 🔁 ETL Flow

### 1️⃣ Extract
- Uses **HttpSensor** to check API availability  
- Uses **SimpleHttpOperator** to fetch JSON weather data  
- City is parameterized  

---

### 2️⃣ Transform
- Convert Kelvin to Fahrenheit  
- Extract relevant weather fields  
- Create structured Pandas DataFrame  

---

### 3️⃣ Schema Validation & Data Quality

Validates:

- Required JSON keys  
- Required `main` fields  
- Temperature realistic range (200K–350K)  
- Humidity range (0–100)  
- Wind speed non-negative  

---

### 4️⃣ Load

- Stores **Partitioned Parquet** in S3  
- Partitioned by execution date  
- Environment-based bucket selection  

---

## 🗂 S3 Storage Structure


---

## ✨ Additional Features Implemented

### 📧 Email Alerts
- Email notifications configured for task failures  
- Alerts triggered automatically on retry exhaustion  
- Uses Airflow’s built-in email configuration  
- Enables production-grade monitoring  

---

### 🌍 Parameterized City
- Supports dynamic city configuration  
- Controlled via environment variables or Airflow Variables  

---

### 🌍 Environment Configuration
- Bucket selection dynamically changes based on environment  
- Supports:
  - `weather-etl-dev-nikhil`
  - `weather-etl-nikhil`

---

## 🧠 Resume Value

This project demonstrates:

✔ Apache Airflow orchestration  
✔ REST API integration  
✔ Schema validation & data quality checks  
✔ Partitioned Parquet data lake design  
✔ AWS S3 cloud integration  
✔ Environment-based configuration (dev/prod)  
✔ Parameterized pipelines  
✔ Email alerting & retry strategy  
✔ Production-style ETL architecture  

---

## 📌 Future Improvements (Next Level)

- Add CI/CD for DAG deployment  
- Add unit tests for transform function  
- Integrate Athena for querying Parquet files  
- Add data catalog integration  
- Add monitoring dashboard  

---
