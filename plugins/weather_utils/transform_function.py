import os
import pandas as pd
from datetime import datetime

def kelvin_to_fahrenheit(temp_k):
    return (temp_k - 273.15) * (9/5) + 32
def validate_weather_schema(data):
    # Required top-level keys
    required_keys = ["name", "weather", "main", "wind", "dt", "timezone"]

    for key in required_keys:
        if key not in data:
            raise ValueError(f"Missing required key: {key}")

    # Validate main block
    if not isinstance(data["main"], dict):
        raise ValueError("Invalid schema: 'main' must be dictionary")

    required_main_keys = ["temp", "feels_like", "temp_min", "temp_max", "pressure", "humidity"]

    for key in required_main_keys:
        if key not in data["main"]:
            raise ValueError(f"Missing main field: {key}")
        if data["main"][key] is None:
            raise ValueError(f"Null value in main field: {key}")
    
    # Validate weather array
    if not isinstance(data["weather"], list) or len(data["weather"]) == 0:
        raise ValueError("Invalid weather structure")

    
    # Range validation
    temp_k = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]

    if temp_k < 200 or temp_k > 350:
        raise ValueError("Temperature out of realistic Kelvin range")

    if humidity < 0 or humidity > 100:
        raise ValueError("Humidity out of range (0–100)")

    if wind_speed < 0:
        raise ValueError("Wind speed cannot be negative")
    print("Schema validation passed ")
 
def transform_load_data(task_instance):
    env=os.getenv("ENVIRONMENT","prod")
    if env=="prod":
        bucket="weather-etl-nikhil"
    else:
        bucket = "weather-etl-dev-nikhil"
    data = task_instance.xcom_pull(task_ids="extract_weather_data")
    validate_weather_schema(data)

    city = data["name"]
    weather_description = data["weather"][0]["description"]
    temp_f = kelvin_to_fahrenheit(data["main"]["temp"])
    feels_like_f = kelvin_to_fahrenheit(data["main"]["feels_like"])
    min_temp_f = kelvin_to_fahrenheit(data["main"]["temp_min"])
    max_temp_f = kelvin_to_fahrenheit(data["main"]["temp_max"])
    pressure = data["main"]["pressure"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]
    time_of_record = datetime.utcfromtimestamp(data["dt"] + data["timezone"])
    record_date= time_of_record.date()
    df = pd.DataFrame([{
        "City": city,
        "Description": weather_description,
        "Temperature (F)": temp_f,
        "Feels Like (F)": feels_like_f,
        "Min Temp (F)": min_temp_f,
        "Max Temp (F)": max_temp_f,
        "Pressure": pressure,
        "Humidity": humidity,
        "Wind Speed": wind_speed,
        "Time of Record": time_of_record,
	"date":str(record_date)
    }])

# ---- Parquet + partitioned S3 path ----
    
    s3_path = f"s3://{bucket}/weather/"
    df.to_parquet(s3_path, index=False, engine="pyarrow",partition_cols=["date"])
    print("Weather data written to S3 (partitioned by date")


