import numpy as np
import pandas as pd
import pymysql
from sqlalchemy import create_engine, text
from sqlalchemy.types import *

# Define your MySQL connection parameters
MYSQL_USER = "root"
MYSQL_PASSWORD = "Abrakadabra69!"
MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_DATABASE = "grand_tours"

connection = pymysql.connect(
    host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, password=MYSQL_PASSWORD
)
cursor = connection.cursor()

cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DATABASE}")

cursor.close()
connection.close()

engine = create_engine(
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
)

df_ids = pd.read_csv(
    "../strava/strava_ids_fin.csv", usecols=["name", "strava_id"]
).dropna()

df_name_schema = {
    "name": String(64),
    "strava_id": Integer,
}

with engine.connect() as connection:

    df_ids.to_sql(
        "strava_names",
        connection,
        if_exists="replace",
        dtype=df_name_schema,
        index=False,
    )

print("database uploaded")

with engine.connect() as connection:
    connection.execute(text(" ALTER TABLE strava_names ADD PRIMARY KEY(strava_id); "))

connection.close()
engine.dispose()
