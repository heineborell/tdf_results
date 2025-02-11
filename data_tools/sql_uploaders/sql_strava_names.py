import numpy as np
import pandas as pd
from sqlalchemy import Column, Integer, String
from sqlalchemy.types import *

from grand_tours import sql_upload

names = sql_upload.SqlUploader(
    "root", "Abrakadabra69!", "127.0.0.1", 3306, "grand_tours"
)

df_ids = pd.read_csv(
    "~/iCloud/Research/Data_Science/Projects/data/strava/strava_ids.csv",
    usecols=["name", "strava_id"],
).dropna()

df_name_schema = {
    "name": String(64),
    "strava_id": Integer(),  # Added primary key to 'strava_id'
}

names.direct_loader(df_ids)

names.csv_uploader(df_schema=df_name_schema, table_name="strava_names")

