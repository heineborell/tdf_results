import numpy as np
import pandas as pd
import pymysql
from sqlalchemy import create_engine

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

query_all_names = "SELECT DISTINCT(`name`) FROM tdf_database "

cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DATABASE}")

cursor.close()
connection.close()


df = pd.read_csv("strava_ids_fin.csv")
df["name"] = df["name"].str.replace(r"\s{2,}", "")


engine = create_engine(
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
)

with engine.connect() as connection:
    df.to_sql("strava_ids", connection, if_exists="append", index=False)

print("database uploaded")

connection.close()
engine.dispose()
